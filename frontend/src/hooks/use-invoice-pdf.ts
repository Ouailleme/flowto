import { useMutation } from "@tanstack/react-query"
import { apiClient } from "@/lib/api"
import { toast } from "@/hooks/use-toast"

export function useDownloadInvoicePDF() {
  return useMutation({
    mutationFn: async (invoiceId: string) => {
      const response = await apiClient.get(`/invoices/${invoiceId}/pdf`, {
        responseType: "blob",
      })
      return response.data
    },
    onSuccess: (data, invoiceId) => {
      // Create download link
      const url = window.URL.createObjectURL(new Blob([data]))
      const link = document.createElement("a")
      link.href = url
      link.setAttribute("download", `facture-${invoiceId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      toast({
        title: "PDF téléchargé",
        description: "La facture a été téléchargée avec succès",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.response?.data?.detail || "Impossible de télécharger le PDF",
        variant: "destructive",
      })
    },
  })
}

export function useSendInvoiceEmail() {
  return useMutation({
    mutationFn: async ({
      invoiceId,
      email,
      subject,
      message,
    }: {
      invoiceId: string
      email: string
      subject?: string
      message?: string
    }) => {
      const { data } = await apiClient.post(`/invoices/${invoiceId}/send`, {
        recipient_email: email,
        subject,
        message,
      })
      return data
    },
    onSuccess: () => {
      toast({
        title: "Email envoyé",
        description: "La facture a été envoyée par email avec succès",
      })
    },
    onError: (error: any) => {
      toast({
        title: "Erreur",
        description: error.response?.data?.detail || "Impossible d'envoyer l'email",
        variant: "destructive",
      })
    },
  })
}

