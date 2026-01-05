"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useAuth } from "@/hooks/use-auth"
import { ArrowLeft, Sparkles } from "lucide-react"

export default function RegisterPage() {
  const { register, isRegisterLoading } = useAuth()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [fullName, setFullName] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (password !== confirmPassword) {
      alert("Les mots de passe ne correspondent pas")
      return
    }

    register({ email, password, full_name: fullName })
  }

  return (
    <div className="flex min-h-screen">
      {/* Left side - Form */}
      <div className="flex w-full flex-col justify-center px-4 py-12 sm:px-6 lg:w-1/2 lg:px-20 xl:px-24">
        <div className="mx-auto w-full max-w-sm">
          {/* Back to home */}
          <Link
            href="/"
            className="mb-8 inline-flex items-center text-sm text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Retour à l'accueil
          </Link>

          {/* Logo */}
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold">FinanceAI</h1>
            </div>
            <h2 className="text-3xl font-bold tracking-tight">
              Créer un compte
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Commencez à automatiser votre comptabilité gratuitement
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="fullName">Nom complet</Label>
              <Input
                id="fullName"
                type="text"
                placeholder="Jean Dupont"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                autoComplete="name"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email professionnel</Label>
              <Input
                id="email"
                type="email"
                placeholder="vous@entreprise.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Mot de passe</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="new-password"
                minLength={8}
              />
              <p className="text-xs text-muted-foreground">
                Minimum 8 caractères
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmPassword">Confirmer le mot de passe</Label>
              <Input
                id="confirmPassword"
                type="password"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                autoComplete="new-password"
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={isRegisterLoading}
            >
              {isRegisterLoading ? "Création..." : "Créer mon compte"}
            </Button>

            <p className="text-xs text-center text-muted-foreground">
              En créant un compte, vous acceptez nos{" "}
              <Link href="/legal/terms" className="text-primary hover:underline">
                conditions d'utilisation
              </Link>{" "}
              et notre{" "}
              <Link href="/legal/privacy" className="text-primary hover:underline">
                politique de confidentialité
              </Link>
              .
            </p>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-background px-2 text-muted-foreground">
                ou
              </span>
            </div>
          </div>

          {/* Sign in link */}
          <div className="text-center text-sm">
            <span className="text-muted-foreground">
              Déjà un compte ?{" "}
            </span>
            <Link href="/auth/login" className="text-primary hover:underline">
              Se connecter
            </Link>
          </div>
        </div>
      </div>

      {/* Right side - Benefits */}
      <div className="hidden lg:block lg:w-1/2 bg-gradient-to-br from-blue-500 to-purple-500 relative overflow-hidden">
        <div className="absolute inset-0 flex items-center justify-center p-12">
          <div className="max-w-md text-white">
            <h3 className="text-4xl font-bold mb-6">
              Pourquoi FinanceAI ?
            </h3>
            <ul className="space-y-4 text-lg">
              <li className="flex items-start gap-3">
                <Sparkles className="h-6 w-6 mt-1 flex-shrink-0" />
                <span>Catégorisation automatique avec IA (95%+ précision)</span>
              </li>
              <li className="flex items-start gap-3">
                <Sparkles className="h-6 w-6 mt-1 flex-shrink-0" />
                <span>Rapprochement bancaire en 1 clic</span>
              </li>
              <li className="flex items-start gap-3">
                <Sparkles className="h-6 w-6 mt-1 flex-shrink-0" />
                <span>Relances automatiques personnalisées</span>
              </li>
              <li className="flex items-start gap-3">
                <Sparkles className="h-6 w-6 mt-1 flex-shrink-0" />
                <span>Économisez 90% de temps sur votre comptabilité</span>
              </li>
            </ul>
            
            <div className="mt-8 p-4 bg-white/10 backdrop-blur-sm rounded-lg">
              <p className="text-sm font-semibold mb-1">Essai gratuit 14 jours</p>
              <p className="text-sm text-white/80">
                Aucune carte bancaire requise. Annulez à tout moment.
              </p>
            </div>
          </div>
        </div>
        
        {/* Decorative circles */}
        <div className="absolute top-20 right-20 h-64 w-64 rounded-full bg-white/10 blur-3xl" />
        <div className="absolute bottom-20 left-20 h-96 w-96 rounded-full bg-white/10 blur-3xl" />
      </div>
    </div>
  )
}


