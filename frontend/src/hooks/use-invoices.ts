"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api, getAccessToken } from "@/lib/api"
import { toast } from "@/hooks/use-toast"

export function useInvoices(params?: any) {
  return useQuery({
    queryKey: ["invoices", params],
    queryFn: () => api.invoices.list(params),
    enabled: !!getAccessToken(), // Only fetch if authenticated
    staleTime: 30000, // 30 seconds
  })
}

export function useCreateInvoice() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: api.invoices.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["invoices"] })
      toast({
        title: "Facture créée",
        description: "La facture a été créée avec succès",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.detail || "Impossible de créer la facture",
        variant: "destructive",
      })
    },
  })
}

export function useUpdateInvoice() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      api.invoices.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["invoices"] })
      toast({
        title: "Facture mise à jour",
        description: "La facture a été mise à jour avec succès",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.detail || "Impossible de mettre à jour la facture",
        variant: "destructive",
      })
    },
  })
}

export function useDeleteInvoice() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: api.invoices.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["invoices"] })
      toast({
        title: "Facture supprimée",
        description: "La facture a été supprimée avec succès",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.detail || "Impossible de supprimer la facture",
        variant: "destructive",
      })
    },
  })
}

