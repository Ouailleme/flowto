"use client"

import { useState } from "react"
import { useTransactions, useCategorizeTransaction, useBulkCategorize } from "@/hooks/use-transactions"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Sparkles, Search, Filter, Download } from "lucide-react"
import { formatCurrency, formatDate } from "@/lib/utils"

export default function TransactionsPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState("")
  
  const { data, isLoading } = useTransactions({ page, page_size: 20, search })
  const { mutate: categorize } = useCategorizeTransaction()
  const { mutate: bulkCategorize, isPending: isBulkCategorizing } = useBulkCategorize()

  const transactions = data?.transactions || []
  const totalPages = data?.total_pages || 1

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Transactions</h1>
          <p className="text-muted-foreground">
            Toutes vos transactions bancaires synchronisées
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            disabled={isBulkCategorizing}
            onClick={() => bulkCategorize(50)}
          >
            <Sparkles className="mr-2 h-4 w-4" />
            {isBulkCategorizing ? "Catégorisation..." : "Catégoriser tout"}
          </Button>
          <Button variant="outline" size="sm">
            <Download className="mr-2 h-4 w-4" />
            Exporter
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-3">
            <CardDescription>Transactions ce mois</CardDescription>
            <CardTitle className="text-2xl">{data?.total || 0}</CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardDescription>Catégorisées</CardDescription>
            <CardTitle className="text-2xl">
              {transactions.filter((t: any) => t.category).length}
            </CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardDescription>Rapprochées</CardDescription>
            <CardTitle className="text-2xl">
              {transactions.filter((t: any) => t.is_reconciled).length}
            </CardTitle>
          </CardHeader>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Rechercher une transaction..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button variant="outline" size="icon">
              <Filter className="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Description</TableHead>
                <TableHead>Catégorie</TableHead>
                <TableHead className="text-right">Montant</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transactions.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center py-8">
                    <p className="text-muted-foreground">Aucune transaction</p>
                  </TableCell>
                </TableRow>
              ) : (
                transactions.map((transaction: any) => (
                  <TableRow key={transaction.id}>
                    <TableCell className="font-medium">
                      {formatDate(transaction.date)}
                    </TableCell>
                    <TableCell>
                      <div>
                        <p className="font-medium">{transaction.description}</p>
                        {transaction.category && (
                          <p className="text-xs text-muted-foreground">
                            Confiance: {Math.round(parseFloat(transaction.category_confidence || 0) * 100)}%
                          </p>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      {transaction.category ? (
                        <Badge variant="secondary">
                          {transaction.category.replace(/_/g, " ")}
                        </Badge>
                      ) : (
                        <Badge variant="outline">Non catégorisé</Badge>
                      )}
                    </TableCell>
                    <TableCell className="text-right font-medium">
                      <span
                        className={
                          parseFloat(transaction.amount) > 0
                            ? "text-green-600"
                            : "text-gray-900 dark:text-white"
                        }
                      >
                        {formatCurrency(transaction.amount, transaction.currency)}
                      </span>
                    </TableCell>
                    <TableCell>
                      {transaction.is_reconciled ? (
                        <Badge variant="success">Rapproché</Badge>
                      ) : (
                        <Badge variant="warning">En attente</Badge>
                      )}
                    </TableCell>
                    <TableCell className="text-right">
                      {!transaction.category && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => categorize(transaction.id)}
                        >
                          <Sparkles className="h-4 w-4" />
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-muted-foreground">
                Page {page} sur {totalPages}
              </p>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage(page - 1)}
                  disabled={page === 1}
                >
                  Précédent
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage(page + 1)}
                  disabled={page === totalPages}
                >
                  Suivant
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}


