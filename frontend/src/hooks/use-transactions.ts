"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api, getAccessToken } from "@/lib/api"
import { toast } from "@/hooks/use-toast"

export function useTransactions(params?: any) {
  return useQuery({
    queryKey: ["transactions", params],
    queryFn: () => api.transactions.list(params),
    enabled: !!getAccessToken(), // Only fetch if authenticated
    staleTime: 30000, // 30 seconds
  })
}

export function useTransaction(id: string) {
  return useQuery({
    queryKey: ["transactions", id],
    queryFn: () => api.transactions.get(id),
    enabled: !!id && !!getAccessToken(), // Only fetch if authenticated and id is provided
  })
}

export function useCategorizeTransaction() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: api.categorization.categorize,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["transactions"] })
      toast({
        title: "Transaction catégorisée",
        description: "La catégorie a été attribuée avec succès",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.detail || "Impossible de catégoriser la transaction",
        variant: "destructive",
      })
    },
  })
}

export function useBulkCategorize() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (limit?: number) => api.categorization.bulk(limit),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["transactions"] })
      toast({
        title: "Catégorisation terminée",
        description: `${data.categorized} transactions catégorisées`,
      })
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.detail || "Impossible de catégoriser les transactions",
        variant: "destructive",
      })
    },
  })
}

export function useCategoryBreakdown() {
  return useQuery({
    queryKey: ["categorization", "breakdown"],
    queryFn: api.categorization.breakdown,
    enabled: !!getAccessToken(), // Only fetch if authenticated
    staleTime: 60000, // 1 minute
  })
}

