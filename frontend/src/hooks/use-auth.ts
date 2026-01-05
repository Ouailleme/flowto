"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api, setAccessToken, clearAuth, getAccessToken } from "@/lib/api"
import { useRouter } from "next/navigation"
import { toast } from "@/hooks/use-toast"

export interface User {
  id: string
  email: string
  full_name?: string
  is_active: boolean
}

export function useAuth() {
  const router = useRouter()
  const queryClient = useQueryClient()

  // Get current user
  const { data: user, isLoading, error } = useQuery<User>({
    queryKey: ["auth", "me"],
    queryFn: api.auth.me,
    enabled: !!getAccessToken(),
    retry: false,
  })

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      api.auth.login(email, password),
    onSuccess: (data) => {
      setAccessToken(data.access_token)
      queryClient.invalidateQueries({ queryKey: ["auth", "me"] })
      toast({
        title: "Connexion réussie",
        description: "Bienvenue !",
      })
      router.push("/dashboard")
    },
    onError: (error: any) => {
      toast({
        title: "Erreur de connexion",
        description: error.detail || "Email ou mot de passe incorrect",
        variant: "destructive",
      })
    },
  })

  // Register mutation
  const registerMutation = useMutation({
    mutationFn: (data: { email: string; password: string; full_name?: string }) =>
      api.auth.register(data),
    onSuccess: () => {
      toast({
        title: "Inscription réussie",
        description: "Vous pouvez maintenant vous connecter",
      })
      router.push("/auth/login")
    },
    onError: (error: any) => {
      toast({
        title: "Erreur d'inscription",
        description: error.detail || "Une erreur est survenue",
        variant: "destructive",
      })
    },
  })

  // Logout
  const logout = () => {
    clearAuth()
    queryClient.clear()
    router.push("/auth/login")
    toast({
      title: "Déconnexion",
      description: "À bientôt !",
    })
  }

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    login: loginMutation.mutate,
    register: registerMutation.mutate,
    logout,
    isLoginLoading: loginMutation.isPending,
    isRegisterLoading: registerMutation.isPending,
  }
}


