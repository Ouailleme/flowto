"use client"

import { useState } from "react"
import { useAuth } from "@/hooks/use-auth"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Building2,
  RefreshCw,
  Plus,
  Wallet,
  CheckCircle,
  AlertCircle,
  Trash2,
} from "lucide-react"
import { formatCurrency, formatDate } from "@/lib/utils"
import { apiClient } from "@/lib/api"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "@/hooks/use-toast"

interface BankAccount {
  id: string
  bank_name: string
  account_type: string
  iban?: string
  balance: number
  currency: string
  is_active: boolean
  bridge_account_id?: string
  last_sync_at?: string
  created_at: string
}

export default function BanksPage() {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [syncingAccounts, setSyncingAccounts] = useState<Set<string>>(new Set())

  // Fetch bank accounts
  const { data: accountsData, isLoading } = useQuery({
    queryKey: ["bank-accounts"],
    queryFn: async () => {
      const { data } = await apiClient.get<{ accounts: BankAccount[]; total: number }>(
        "/banks/"
      )
      return data
    },
  })

  // Connect Bridge mutation
  const connectBridgeMutation = useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post<{ connect_url: string }>(
        "/banks/connect/initiate"
      )
      return data
    },
    onSuccess: (data) => {
      // Open Bridge connect URL in new window
      window.open(data.connect_url, "_blank", "width=800,height=600")
      toast({
        title: "Connexion bancaire initiée",
        description: "Suivez les instructions dans la fenêtre ouverte",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.response?.data?.detail || "Impossible de se connecter à Bridge",
        variant: "destructive",
      })
    },
  })

  // Sync transactions mutation
  const syncMutation = useMutation({
    mutationFn: async (accountId: string) => {
      const { data } = await apiClient.post(`/banks/${accountId}/sync`)
      return data
    },
    onSuccess: (data, accountId) => {
      queryClient.invalidateQueries({ queryKey: ["bank-accounts"] })
      queryClient.invalidateQueries({ queryKey: ["transactions"] })
      setSyncingAccounts(prev => {
        const next = new Set(prev)
        next.delete(accountId)
        return next
      })
      toast({
        title: "Synchronisation réussie",
        description: `${data.new_count} nouvelles transactions importées`,
      })
    },
    onError: (error: any, accountId) => {
      setSyncingAccounts(prev => {
        const next = new Set(prev)
        next.delete(accountId)
        return next
      })
      toast({
        title: "Erreur de synchronisation",
        description: error.response?.data?.detail || "Impossible de synchroniser",
        variant: "destructive",
      })
    },
  })

  const handleSync = (accountId: string) => {
    setSyncingAccounts(prev => new Set(prev).add(accountId))
    syncMutation.mutate(accountId)
  }

  const accounts = accountsData?.accounts || []
  const connectedAccounts = accounts.filter(acc => acc.bridge_account_id)
  const manualAccounts = accounts.filter(acc => !acc.bridge_account_id)

  if (isLoading) {
    return (
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Comptes bancaires</h1>
          <p className="text-muted-foreground">Chargement...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Comptes bancaires</h1>
          <p className="text-muted-foreground">
            Gérez vos connexions bancaires et synchronisez vos transactions
          </p>
        </div>
        <Button
          onClick={() => connectBridgeMutation.mutate()}
          disabled={connectBridgeMutation.isPending}
        >
          <Plus className="mr-2 h-4 w-4" />
          Connecter une banque
        </Button>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Comptes connectés
                </p>
                <p className="text-3xl font-bold mt-2">{connectedAccounts.length}</p>
              </div>
              <Building2 className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Solde total</p>
                <p className="text-3xl font-bold mt-2">
                  {formatCurrency(
                    accounts.reduce((sum, acc) => sum + acc.balance, 0),
                    "EUR"
                  )}
                </p>
              </div>
              <Wallet className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Dernière sync</p>
                <p className="text-sm font-medium mt-2">
                  {connectedAccounts.length > 0 &&
                  connectedAccounts[0].last_sync_at
                    ? formatDate(new Date(connectedAccounts[0].last_sync_at))
                    : "Jamais"}
                </p>
              </div>
              <RefreshCw className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Connected Accounts */}
      {connectedAccounts.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Comptes synchronisés (Bridge)</h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {connectedAccounts.map((account) => (
              <Card key={account.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      <Building2 className="h-5 w-5 text-primary" />
                      <div>
                        <CardTitle className="text-lg">{account.bank_name}</CardTitle>
                        <CardDescription className="text-xs mt-1">
                          {account.account_type}
                        </CardDescription>
                      </div>
                    </div>
                    {account.is_active ? (
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    ) : (
                      <AlertCircle className="h-5 w-5 text-red-600" />
                    )}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Balance */}
                    <div>
                      <p className="text-2xl font-bold">
                        {formatCurrency(account.balance, account.currency)}
                      </p>
                      {account.iban && (
                        <p className="text-xs text-muted-foreground mt-1">
                          {account.iban.slice(0, 4)}***{account.iban.slice(-4)}
                        </p>
                      )}
                    </div>

                    {/* Last Sync */}
                    {account.last_sync_at && (
                      <p className="text-xs text-muted-foreground">
                        Dernière sync :{" "}
                        {formatDate(new Date(account.last_sync_at))}
                      </p>
                    )}

                    {/* Actions */}
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        className="flex-1"
                        onClick={() => handleSync(account.id)}
                        disabled={syncingAccounts.has(account.id)}
                      >
                        {syncingAccounts.has(account.id) ? (
                          <>
                            <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                            Sync...
                          </>
                        ) : (
                          <>
                            <RefreshCw className="mr-2 h-4 w-4" />
                            Synchroniser
                          </>
                        )}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Manual Accounts */}
      {manualAccounts.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Comptes manuels</h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {manualAccounts.map((account) => (
              <Card key={account.id}>
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <Wallet className="h-5 w-5 text-muted-foreground" />
                    <div>
                      <CardTitle className="text-lg">{account.bank_name}</CardTitle>
                      <CardDescription className="text-xs">
                        {account.account_type}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-2xl font-bold">
                      {formatCurrency(account.balance, account.currency)}
                    </p>
                    <Badge variant="outline">Manuel</Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {accounts.length === 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <Building2 className="h-16 w-16 text-muted-foreground mb-4" />
            <h3 className="text-xl font-semibold mb-2">
              Aucun compte bancaire connecté
            </h3>
            <p className="text-muted-foreground text-center mb-6 max-w-md">
              Connectez votre banque via Bridge pour synchroniser automatiquement vos
              transactions et simplifier votre comptabilité.
            </p>
            <Button
              size="lg"
              onClick={() => connectBridgeMutation.mutate()}
              disabled={connectBridgeMutation.isPending}
            >
              <Plus className="mr-2 h-5 w-5" />
              Connecter ma première banque
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

