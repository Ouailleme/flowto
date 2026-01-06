"use client"

import { useAuth } from "@/hooks/use-auth"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import {
  LayoutDashboard,
  Receipt,
  CreditCard,
  Settings,
  LogOut,
  Sparkles,
  Menu,
  Building2,
} from "lucide-react"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { user, isLoading, isAuthenticated, logout } = useAuth()
  const router = useRouter()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/auth/login")
    }
  }, [isLoading, isAuthenticated, router])

  // Prevent hydration mismatch by not rendering until mounted
  if (!mounted || isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-card hidden lg:block">
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex items-center gap-2 p-6 border-b">
            <Sparkles className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold">Flowto</span>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            <NavLink href="/dashboard" icon={LayoutDashboard}>
              Tableau de bord
            </NavLink>
            <NavLink href="/dashboard/banks" icon={Building2}>
              Banques
            </NavLink>
            <NavLink href="/dashboard/transactions" icon={CreditCard}>
              Transactions
            </NavLink>
            <NavLink href="/dashboard/invoices" icon={Receipt}>
              Factures
            </NavLink>
            <NavLink href="/dashboard/settings" icon={Settings}>
              Paramètres
            </NavLink>
          </nav>

          {/* User section */}
          <div className="border-t p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="text-sm">
                <p className="font-medium">{user?.full_name || user?.email}</p>
                <p className="text-xs text-muted-foreground">{user?.email}</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              className="w-full justify-start"
              onClick={logout}
            >
              <LogOut className="mr-2 h-4 w-4" />
              Déconnexion
            </Button>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="container mx-auto p-6 max-w-7xl">
          {children}
        </div>
      </main>
    </div>
  )
}

function NavLink({
  href,
  icon: Icon,
  children,
}: {
  href: string
  icon: React.ElementType
  children: React.ReactNode
}) {
  return (
    <Link
      href={href}
      className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground transition-colors"
    >
      <Icon className="h-4 w-4" />
      {children}
    </Link>
  )
}

