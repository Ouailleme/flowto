# 🎨 DESIGN SYSTEM 2026 - FinanceAI

## 🎯 PHILOSOPHIE: "Beautiful Simplicity Meets Intelligence"

Notre design combine:
- ✨ **Minimalisme Stratégique** - Chaque élément a un but
- 🤖 **IA Invisible** - L'intelligence qui aide sans distraire  
- ♿ **Accessibilité Universelle** - Pour tous, sans exception
- 🌍 **Éco-Responsable** - Performance optimale, empreinte minimale
- 💫 **Micro-Interactions Délicates** - Feedback instantané, animations fluides

---

## 🎨 STACK DESIGN 2026

### Core Technologies
```json
{
  "framework": "Next.js 15 (App Router + React 19)",
  "language": "TypeScript strict",
  "styling": "Tailwind CSS 4.0",
  "components": "shadcn/ui (Radix UI primitives)",
  "animations": "Framer Motion + CSS animations",
  "icons": "Lucide React (optimized)",
  "charts": "Recharts + D3.js (for complex viz)",
  "forms": "React Hook Form + Zod",
  "state": "Zustand + TanStack Query",
  "accessibility": "WCAG 2.2 Level AA"
}
```

### Pourquoi ces choix ?
- **shadcn/ui** : Composants accessibles, personnalisables, 0 runtime cost
- **Framer Motion** : Animations performantes, gestes naturels
- **Tailwind 4.0** : JIT compiler, CSS-in-JS natif, performance optimale
- **Lucide** : 1000+ icônes, tree-shaking automatique, cohérence visuelle

---

## 🎨 SYSTÈME DE COULEURS

### Palette Principale (Adaptative)

**Light Mode** (Par défaut)
```css
--primary: 220 90% 56%;        /* Bleu confiance (fintech) */
--primary-foreground: 0 0% 100%;

--secondary: 210 40% 96%;      /* Gris doux background */
--secondary-foreground: 222 47% 11%;

--accent: 142 76% 36%;         /* Vert succès */
--accent-foreground: 0 0% 100%;

--destructive: 0 84% 60%;      /* Rouge alerte */
--destructive-foreground: 0 0% 100%;

--muted: 210 40% 96%;          /* Background subtil */
--muted-foreground: 215 16% 47%;

--card: 0 0% 100%;
--card-foreground: 222 47% 11%;

--border: 214 32% 91%;
--input: 214 32% 91%;
--ring: 220 90% 56%;
```

**Dark Mode** (Auto + Manuel)
```css
--primary: 220 90% 60%;        /* Bleu plus lumineux */
--primary-foreground: 0 0% 100%;

--secondary: 217 33% 17%;      /* Gris sombre doux */
--secondary-foreground: 210 40% 98%;

--accent: 142 76% 40%;         /* Vert plus vif */
--accent-foreground: 0 0% 100%;

--muted: 217 33% 17%;
--muted-foreground: 215 20% 65%;

--card: 222 47% 11%;
--card-foreground: 210 40% 98%;

--background: 222 47% 9%;      /* Noir bleuté */
--foreground: 210 40% 98%;

--border: 217 33% 20%;
```

### Couleurs Sémantiques (Finances)
```css
--success: 142 76% 36%;        /* Vert - Positif, Payé */
--warning: 38 92% 50%;         /* Orange - Attention, En attente */
--error: 0 84% 60%;            /* Rouge - Négatif, En retard */
--info: 199 89% 48%;           /* Cyan - Information */
--neutral: 215 16% 47%;        /* Gris - Neutre */
```

### Gradients (Subtils)
```css
--gradient-primary: linear-gradient(135deg, hsl(220 90% 56%) 0%, hsl(220 90% 66%) 100%);
--gradient-success: linear-gradient(135deg, hsl(142 76% 36%) 0%, hsl(142 76% 46%) 100%);
--gradient-hero: linear-gradient(180deg, hsl(0 0% 100%) 0%, hsl(210 40% 98%) 100%);
```

---

## 📐 TYPOGRAPHIE

### Font Stack
```css
/* Primary: Inter (system-ui fallback) */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;

/* Monospace (chiffres, code) */
font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;

/* Display (Headings large) */
font-family: 'Cal Sans', 'Inter', sans-serif;
```

### Scale (Tailwind)
```
text-xs:    12px / 16px
text-sm:    14px / 20px
text-base:  16px / 24px (default)
text-lg:    18px / 28px
text-xl:    20px / 28px
text-2xl:   24px / 32px
text-3xl:   30px / 36px
text-4xl:   36px / 40px
```

### Font Weights
```
font-normal:   400 (body text)
font-medium:   500 (emphasis)
font-semibold: 600 (buttons, labels)
font-bold:     700 (headings)
```

### Hiérarchie
```tsx
<h1>: text-4xl font-bold tracking-tight
<h2>: text-3xl font-semibold
<h3>: text-2xl font-semibold
<h4>: text-xl font-semibold
<p>:  text-base font-normal
<small>: text-sm text-muted-foreground
```

---

## 🧱 COMPOSANTS

### 1. Cards (Omnipresents)
```tsx
// Variant 1: Dashboard Card
<Card className="border-none shadow-sm hover:shadow-md transition-shadow">
  <CardHeader>
    <CardTitle>Solde Total</CardTitle>
    <CardDescription>Tous comptes confondus</CardDescription>
  </CardHeader>
  <CardContent>
    <div className="text-3xl font-bold">45 234,56 €</div>
    <p className="text-sm text-green-600 flex items-center gap-1">
      <TrendingUp className="h-4 w-4" />
      +12.5% ce mois
    </p>
  </CardContent>
</Card>

// Variant 2: Glassmorphism (premium)
<Card className="bg-white/80 backdrop-blur-lg border-white/20">
  ...
</Card>
```

### 2. Buttons (États clairs)
```tsx
// Primary
<Button>Synchroniser</Button>

// Secondary
<Button variant="secondary">Annuler</Button>

// Destructive
<Button variant="destructive">Supprimer</Button>

// Ghost (actions subtiles)
<Button variant="ghost" size="sm">
  <Settings className="h-4 w-4" />
</Button>

// Loading state (auto)
<Button disabled>
  <Loader2 className="h-4 w-4 animate-spin mr-2" />
  Chargement...
</Button>
```

### 3. Data Tables (Performance)
```tsx
<DataTable
  columns={columns}
  data={transactions}
  pagination
  sorting
  filtering
  // Virtualization pour 10k+ rows
  virtualized={data.length > 1000}
/>
```

### 4. Charts (Beautiful + Accessible)
```tsx
// Recharts avec palette custom
<ResponsiveContainer width="100%" height={350}>
  <AreaChart data={cashflowData}>
    <defs>
      <linearGradient id="colorAmount" x1="0" y1="0" x2="0" y2="1">
        <stop offset="5%" stopColor="hsl(142 76% 36%)" stopOpacity={0.3}/>
        <stop offset="95%" stopColor="hsl(142 76% 36%)" stopOpacity={0}/>
      </linearGradient>
    </defs>
    <CartesianGrid strokeDasharray="3 3" stroke="hsl(214 32% 91%)" />
    <XAxis dataKey="date" />
    <YAxis />
    <Tooltip content={<CustomTooltip />} />
    <Area
      type="monotone"
      dataKey="amount"
      stroke="hsl(142 76% 36%)"
      fillOpacity={1}
      fill="url(#colorAmount)"
    />
  </AreaChart>
</ResponsiveContainer>
```

### 5. Badges (Status visuels)
```tsx
// Variant par status
<Badge variant="success">Payée</Badge>
<Badge variant="warning">En attente</Badge>
<Badge variant="destructive">En retard</Badge>
<Badge variant="secondary">Brouillon</Badge>
```

### 6. Avatars (Fallback élégant)
```tsx
<Avatar>
  <AvatarImage src="/user.jpg" alt="User" />
  <AvatarFallback className="bg-primary/10 text-primary">
    YM
  </AvatarFallback>
</Avatar>
```

---

## 💫 MICRO-INTERACTIONS

### Principes
1. **Subtilité** - Jamais distrayant
2. **Naturel** - Mouvement physique réaliste
3. **Rapide** - < 300ms
4. **Purposeful** - Chaque animation a un sens

### Animations Standard
```tsx
// Hover sur card
<Card className="transition-all hover:scale-[1.02] hover:shadow-lg">

// Fade in (page load)
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>

// Slide in (sidebar)
<motion.div
  initial={{ x: -300 }}
  animate={{ x: 0 }}
  transition={{ type: "spring", stiffness: 300, damping: 30 }}
>

// Success pulse (après action)
<motion.div
  animate={{
    scale: [1, 1.1, 1],
    boxShadow: [
      "0 0 0 0 rgba(34, 197, 94, 0)",
      "0 0 0 10px rgba(34, 197, 94, 0.2)",
      "0 0 0 0 rgba(34, 197, 94, 0)"
    ]
  }}
  transition={{ duration: 0.6 }}
>
```

### Skeleton Loading (Smart)
```tsx
<Card>
  <CardHeader>
    <Skeleton className="h-4 w-[250px]" />
    <Skeleton className="h-4 w-[200px]" />
  </CardHeader>
  <CardContent>
    <Skeleton className="h-8 w-[150px] mb-2" />
    <Skeleton className="h-4 w-[100px]" />
  </CardContent>
</Card>
```

---

## 📱 RESPONSIVE DESIGN

### Breakpoints (Tailwind)
```
sm:  640px  (tablet)
md:  768px  (tablet landscape)
lg:  1024px (laptop)
xl:  1280px (desktop)
2xl: 1536px (large desktop)
```

### Mobile-First Approach
```tsx
// Sidebar: Hidden mobile, visible desktop
<aside className="hidden lg:block">

// Grid: 1 col mobile, 2 cols tablet, 3 cols desktop
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Font: Smaller mobile, larger desktop
<h1 className="text-2xl md:text-3xl lg:text-4xl">
```

---

## ♿ ACCESSIBILITÉ

### WCAG 2.2 Level AA (Minimum)

**Contraste**
- Texte normal: min 4.5:1
- Texte large: min 3:1
- UI components: min 3:1

**Navigation Clavier**
```tsx
// Tous les éléments interactifs focusable
<button className="focus:ring-2 focus:ring-primary focus:ring-offset-2">

// Skip to content
<a href="#main" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

**ARIA Labels**
```tsx
<Button aria-label="Synchroniser les transactions">
  <RefreshCw className="h-4 w-4" />
</Button>

<input aria-describedby="email-error" />
<span id="email-error" role="alert">Email invalide</span>
```

**Screen Reader Only**
```tsx
<span className="sr-only">Chargement en cours</span>
<Loader2 className="animate-spin" aria-hidden="true" />
```

---

## 🌓 DARK MODE

### Stratégie: Smart + Manual

```tsx
// Provider avec détection système + override utilisateur
<ThemeProvider
  attribute="class"
  defaultTheme="system"
  enableSystem
  disableTransitionOnChange={false}
>

// Toggle élégant
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" size="sm">
      <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuItem onClick={() => setTheme("light")}>
      Light
    </DropdownMenuItem>
    <DropdownMenuItem onClick={() => setTheme("dark")}>
      Dark
    </DropdownMenuItem>
    <DropdownMenuItem onClick={() => setTheme("system")}>
      System
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

---

## 🎯 LAYOUTS

### Dashboard (Principal)
```
┌─────────────────────────────────────────────┐
│ Header: Logo | Search | Notifications | User│
├──────┬──────────────────────────────────────┤
│      │ KPIs (4 cards)                       │
│ Side │ ┌────┬────┬────┬────┐                │
│ bar  │ │ $$ │ ## │ %% │ !! │                │
│      │ └────┴────┴────┴────┘                │
│ Nav  │                                       │
│      │ Chart: Cash Flow                     │
│      │ ┌────────────────────────────────┐   │
│      │ │     📈                          │   │
│      │ └────────────────────────────────┘   │
│      │                                       │
│      │ Recent Transactions                  │
│      │ ┌────────────────────────────────┐   │
│      │ │ Table...                        │   │
│      │ └────────────────────────────────┘   │
└──────┴──────────────────────────────────────┘
```

### Sidebar Navigation
```tsx
<nav className="space-y-1">
  <NavLink href="/dashboard" icon={LayoutDashboard}>
    Dashboard
  </NavLink>
  <NavLink href="/banks" icon={Building2} badge="3">
    Comptes Bancaires
  </NavLink>
  <NavLink href="/transactions" icon={Receipt}>
    Transactions
  </NavLink>
  <NavLink href="/invoices" icon={FileText} badge="12">
    Factures
  </NavLink>
  <NavLink href="/reconciliations" icon={GitCompare} badge="5">
    Rapprochements
  </NavLink>
  
  <Separator className="my-4" />
  
  <NavLink href="/settings" icon={Settings}>
    Paramètres
  </NavLink>
</nav>
```

---

## 🎨 DESIGN TOKENS (CSS Variables)

```css
:root {
  /* Spacing (8px grid) */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  
  /* Border radius */
  --radius-sm: 0.25rem;
  --radius: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  
  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## 📊 EXEMPLES CONCRETS

### Transaction Row (Micro-interactions)
```tsx
<motion.div
  whileHover={{ scale: 1.01, backgroundColor: "hsl(210 40% 98%)" }}
  whileTap={{ scale: 0.99 }}
  className="flex items-center justify-between p-4 rounded-lg cursor-pointer"
>
  <div className="flex items-center gap-3">
    <Avatar className="h-10 w-10">
      <AvatarFallback className="bg-primary/10">
        {getCategoryIcon(transaction.category)}
      </AvatarFallback>
    </Avatar>
    <div>
      <p className="font-medium">{transaction.description}</p>
      <p className="text-sm text-muted-foreground">
        {formatDate(transaction.date, user.language)}
      </p>
    </div>
  </div>
  
  <div className="text-right">
    <p className={cn(
      "font-semibold font-mono",
      transaction.amount > 0 ? "text-success" : "text-foreground"
    )}>
      {formatCurrency(transaction.amount, transaction.currency, user.language)}
    </p>
    {transaction.is_reconciled && (
      <Badge variant="success" className="text-xs">
        Réconciliée
      </Badge>
    )}
  </div>
</motion.div>
```

### Toast Notifications (Smart)
```tsx
// Success
toast({
  title: "✅ Transaction synchronisée",
  description: "12 nouvelles transactions importées",
  variant: "success",
  duration: 3000,
})

// Error with action
toast({
  title: "❌ Erreur de synchronisation",
  description: "Impossible de se connecter à votre banque",
  variant: "destructive",
  action: (
    <ToastAction altText="Réessayer" onClick={retry}>
      Réessayer
    </ToastAction>
  ),
})
```

---

## 🎯 PERFORMANCE

### Metrics Targets
- **FCP** (First Contentful Paint): < 1.8s
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1
- **TTI** (Time to Interactive): < 3.8s

### Optimizations
```tsx
// Image optimization (Next.js)
<Image
  src="/dashboard.png"
  width={1200}
  height={630}
  alt="Dashboard"
  priority // Above fold
  placeholder="blur"
/>

// Code splitting
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <Skeleton className="h-[350px]" />,
  ssr: false // Client-side only
})

// Lazy load
const AdminPanel = lazy(() => import('./AdminPanel'))
```

---

## ✅ CHECKLIST DESIGN

### Avant de coder un composant:
- [ ] Accessible (keyboard, screen reader)
- [ ] Responsive (mobile, tablet, desktop)
- [ ] Dark mode support
- [ ] Loading state
- [ ] Error state
- [ ] Empty state
- [ ] Micro-interactions
- [ ] Performance optimized

---

**DESIGN SYSTEM = BIBLE DU PROJET** 📖

Chaque composant créé doit suivre ces guidelines pour assurer cohérence et qualité.

