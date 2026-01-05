import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles, TrendingUp, Zap } from "lucide-react";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Hero Section */}
      <section className="relative flex min-h-[90vh] items-center justify-center overflow-hidden">
        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900" />
        
        {/* Animated circles */}
        <div className="absolute top-20 left-20 h-72 w-72 rounded-full bg-purple-300/20 blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-20 h-96 w-96 rounded-full bg-blue-300/20 blur-3xl animate-pulse delay-1000" />
        
        <div className="container relative z-10 mx-auto px-4">
          <div className="mx-auto max-w-4xl text-center">
            {/* Badge */}
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-purple-200 bg-purple-50 px-4 py-2 text-sm font-medium text-purple-700 dark:border-purple-800 dark:bg-purple-900/30 dark:text-purple-300">
              <Sparkles className="h-4 w-4" />
              Propulsé par l'Intelligence Artificielle
            </div>
            
            {/* Title */}
            <h1 className="mb-6 text-5xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
              Automatisez votre
              <span className="gradient-text"> comptabilité</span>
              <br />
              en quelques clics
            </h1>
            
            {/* Description */}
            <p className="mb-8 text-xl text-muted-foreground sm:text-2xl">
              FinanceAI révolutionne la gestion financière des PME avec une plateforme
              intelligente qui catégorise, rapproche et relance automatiquement.
            </p>
            
            {/* CTAs */}
            <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button asChild size="lg" className="group">
                <Link href="/auth/register">
                  Commencer gratuitement
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link href="#features">
                  Découvrir les fonctionnalités
                </Link>
              </Button>
            </div>
            
            {/* Social proof */}
            <div className="mt-12 flex items-center justify-center gap-8 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-green-500" />
                <span>90%+ de gain de temps</span>
              </div>
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4 text-yellow-500" />
                <span>Réconciliation en 1 clic</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl mb-4">
              Tout ce dont vous avez besoin
            </h2>
            <p className="text-lg text-muted-foreground">
              Une suite complète d'outils pour automatiser votre comptabilité
            </p>
          </div>
          
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, i) => (
              <div
                key={i}
                className="glass rounded-2xl p-6 hover:shadow-lg transition-shadow"
              >
                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <feature.icon className="h-6 w-6" />
                </div>
                <h3 className="mb-2 text-xl font-semibold">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-r from-purple-500 to-blue-500">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Prêt à transformer votre comptabilité ?
          </h2>
          <p className="text-lg text-white/90 mb-8 max-w-2xl mx-auto">
            Rejoignez des centaines de PME qui ont déjà automatisé leur gestion financière
          </p>
          <Button asChild size="lg" variant="secondary">
            <Link href="/auth/register">
              Essayer gratuitement pendant 14 jours
            </Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>© 2026 FinanceAI. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  );
}

const features = [
  {
    icon: Sparkles,
    title: "Catégorisation IA",
    description: "Catégorisation automatique de vos transactions bancaires avec 95%+ de précision grâce à Claude AI.",
  },
  {
    icon: TrendingUp,
    title: "Rapprochement bancaire",
    description: "Rapprochez vos transactions et factures en 1 clic grâce au fuzzy matching IA.",
  },
  {
    icon: Zap,
    title: "Relances automatiques",
    description: "Envoi automatique de relances personnalisées pour vos factures impayées.",
  },
  {
    icon: ArrowRight,
    title: "Synchronisation bancaire",
    description: "Connectez vos comptes bancaires via Bridge API et synchronisez automatiquement.",
  },
  {
    icon: TrendingUp,
    title: "Prévisions trésorerie",
    description: "Anticipez vos besoins de trésorerie avec des prévisions IA basées sur votre historique.",
  },
  {
    icon: Sparkles,
    title: "Tableau de bord temps réel",
    description: "Visualisez votre santé financière en temps réel avec des graphiques interactifs.",
  },
];


