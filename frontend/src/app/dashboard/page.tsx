"use client"

import { useAuth } from "@/hooks/use-auth"
import { useInvoices } from "@/hooks/use-invoices"
import { useTransactions } from "@/hooks/use-transactions"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  Receipt,
  CreditCard,
  TrendingUp,
  AlertCircle,
  Sparkles,
  ArrowRight,
} from "lucide-react"
import Link from "next/link"
import { formatCurrency } from "@/lib/utils"

export default function DashboardPage() {
  const { user } = useAuth()
  const { data: invoicesData } = useInvoices({ page: 1, page_size: 5 })
  const { data: transactionsData } = useTransactions({ page: 1, page_size: 5 })

  const overdueInvoices = invoicesData?.invoices?.filter(
    (inv: any) => inv.status === "overdue"
  ) || []

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Bonjour {user?.full_name?.split(" ")[0] || "👋"}
        </h1>
        <p className="text-muted-foreground">
          Voici un aperçu de votre activité financière
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Factures en attente"
          value={invoicesData?.invoices?.filter((inv: any) => inv.status === "pending").length || 0}
          icon={Receipt}
          color="text-yellow-600"
        />
        <StatsCard
          title="Factures en retard"
          value={overdueInvoices.length}
          icon={AlertCircle}
          color="text-red-600"
        />
        <StatsCard
          title="Transactions ce mois"
          value={transactionsData?.total || 0}
          icon={CreditCard}
          color="text-blue-600"
        />
        <StatsCard
          title="Taux catégorisation"
          value="95%"
          icon={Sparkles}
          color="text-purple-600"
        />
      </div>

      {/* Actions rapides */}
      <Card>
        <CardHeader>
          <CardTitle>Actions rapides</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <ActionCard
              title="Créer une facture"
              description="Nouvelle facture client"
              icon={Receipt}
              href="/dashboard/invoices/new"
            />
            <ActionCard
              title="Catégoriser"
              description="Catégoriser les transactions"
              icon={Sparkles}
              href="/dashboard/transactions?action=categorize"
            />
            <ActionCard
              title="Rapprochements"
              description="Rapprocher transactions et factures"
              icon={TrendingUp}
              href="/dashboard/reconciliations"
            />
          </div>
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Recent Invoices */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Factures récentes</CardTitle>
            <Button variant="ghost" size="sm" asChild>
              <Link href="/dashboard/invoices">
                Voir tout
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </CardHeader>
          <CardContent>
            {invoicesData?.invoices?.length === 0 ? (
              <p className="text-sm text-muted-foreground">Aucune facture</p>
            ) : (
              <div className="space-y-4">
                {invoicesData?.invoices?.slice(0, 5).map((invoice: any) => (
                  <div
                    key={invoice.id}
                    className="flex items-center justify-between"
                  >
                    <div>
                      <p className="font-medium">{invoice.client_name}</p>
                      <p className="text-sm text-muted-foreground">
                        {invoice.invoice_number}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium">
                        {formatCurrency(invoice.total_amount, invoice.currency)}
                      </p>
                      <p className={`text-xs ${
                        invoice.status === "paid"
                          ? "text-green-600"
                          : invoice.status === "overdue"
                          ? "text-red-600"
                          : "text-yellow-600"
                      }`}>
                        {invoice.status}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Transactions */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Transactions récentes</CardTitle>
            <Button variant="ghost" size="sm" asChild>
              <Link href="/dashboard/transactions">
                Voir tout
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </CardHeader>
          <CardContent>
            {transactionsData?.transactions?.length === 0 ? (
              <p className="text-sm text-muted-foreground">Aucune transaction</p>
            ) : (
              <div className="space-y-4">
                {transactionsData?.transactions?.slice(0, 5).map((tx: any) => (
                  <div
                    key={tx.id}
                    className="flex items-center justify-between"
                  >
                    <div className="flex-1">
                      <p className="font-medium text-sm">{tx.description}</p>
                      {tx.category && (
                        <p className="text-xs text-muted-foreground">
                          {tx.category}
                        </p>
                      )}
                    </div>
                    <p
                      className={`font-medium ${
                        tx.amount > 0 ? "text-green-600" : "text-gray-900 dark:text-white"
                      }`}
                    >
                      {formatCurrency(tx.amount, tx.currency)}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function StatsCard({
  title,
  value,
  icon: Icon,
  color,
}: {
  title: string
  value: number | string
  icon: React.ElementType
  color: string
}) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className="text-3xl font-bold mt-2">{value}</p>
          </div>
          <Icon className={`h-8 w-8 ${color}`} />
        </div>
      </CardContent>
    </Card>
  )
}

function ActionCard({
  title,
  description,
  icon: Icon,
  href,
}: {
  title: string
  description: string
  icon: React.ElementType
  href: string
}) {
  return (
    <Link
      href={href}
      className="flex items-start gap-4 rounded-lg border p-4 hover:bg-accent transition-colors"
    >
      <div className="rounded-lg bg-primary/10 p-2">
        <Icon className="h-5 w-5 text-primary" />
      </div>
      <div>
        <h3 className="font-medium">{title}</h3>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
    </Link>
  )
}


