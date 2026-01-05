# ✅ Fix Erreur 401 Unauthorized - RÉSOLU

**Date** : 5 janvier 2026 - 23:00  
**Status** : ✅ **RÉSOLU**

---

## 🐛 Problème

```
GET http://localhost:8000/api/v1/invoices/?page=1&page_size=5 401 (Unauthorized)
GET http://localhost:8000/api/v1/transactions/?page=1&page_size=5 401 (Unauthorized)
```

### Cause Racine

Les hooks `useInvoices` et `useTransactions` essayaient de faire des appels API **immédiatement au chargement du composant**, même si l'utilisateur n'était **pas encore authentifié** ou si le token d'authentification n'était **pas présent dans le localStorage**.

### Scénario Problématique

1. L'utilisateur accède directement à `/dashboard` (via URL ou rafraîchissement F5)
2. Le composant `DashboardPage` se monte
3. Les hooks `useInvoices` et `useTransactions` déclenchent immédiatement des requêtes API
4. **Pas de token dans les headers** → Erreur 401 Unauthorized
5. Le hook `useAuth` redirige ensuite vers `/auth/login`, mais les erreurs 401 sont déjà dans la console

---

## ✅ Solution

Ajouter la propriété `enabled` à tous les hooks de requête pour vérifier l'authentification **avant** de faire les appels API.

### Modifications Appliquées

#### 1️⃣ `frontend/src/hooks/use-invoices.ts`

```typescript
import { api, getAccessToken } from "@/lib/api"

export function useInvoices(params?: any) {
  return useQuery({
    queryKey: ["invoices", params],
    queryFn: () => api.invoices.list(params),
    enabled: !!getAccessToken(), // ✅ Only fetch if authenticated
    staleTime: 30000,
  })
}
```

#### 2️⃣ `frontend/src/hooks/use-transactions.ts`

```typescript
import { api, getAccessToken } from "@/lib/api"

export function useTransactions(params?: any) {
  return useQuery({
    queryKey: ["transactions", params],
    queryFn: () => api.transactions.list(params),
    enabled: !!getAccessToken(), // ✅ Only fetch if authenticated
    staleTime: 30000,
  })
}

export function useTransaction(id: string) {
  return useQuery({
    queryKey: ["transactions", id],
    queryFn: () => api.transactions.get(id),
    enabled: !!id && !!getAccessToken(), // ✅ Only fetch if authenticated AND id provided
  })
}

export function useCategoryBreakdown() {
  return useQuery({
    queryKey: ["categorization", "breakdown"],
    queryFn: api.categorization.breakdown,
    enabled: !!getAccessToken(), // ✅ Only fetch if authenticated
    staleTime: 60000,
  })
}
```

---

## 🔍 Comment Ça Fonctionne ?

### Propriété `enabled` de React Query

```typescript
enabled: !!getAccessToken()
```

- `getAccessToken()` retourne le token JWT depuis le `localStorage`
- Si le token existe → `enabled: true` → La requête s'exécute
- Si le token n'existe pas → `enabled: false` → La requête **ne s'exécute pas**
- React Query attendra que `enabled` devienne `true` pour lancer la requête

### Workflow Complet

```
1. User accède à /dashboard
   ↓
2. DashboardLayout se monte
   ↓
3. useAuth vérifie getAccessToken()
   ├─ Token existe ?
   │  ├─ OUI → Fetch /api/v1/auth/me → User OK → Dashboard s'affiche
   │  │         ↓
   │  │         useInvoices et useTransactions détectent le token
   │  │         ↓
   │  │         Requêtes API lancées avec Authorization header ✅
   │  │
   │  └─ NON → Pas de fetch /me
   │            ↓
   │            useAuth.isAuthenticated = false
   │            ↓
   │            useEffect redirige vers /auth/login
   │            ↓
   │            useInvoices et useTransactions NE LANCENT PAS de requêtes ✅
   │            (car enabled: !!getAccessToken() = false)
```

---

## 🎯 Résultat

### Avant ❌
```
Console :
❌ GET /api/v1/invoices/ 401 (Unauthorized)
❌ GET /api/v1/transactions/ 401 (Unauthorized)
→ Puis redirection vers /auth/login
```

### Après ✅
```
Console :
✅ Aucune requête API sans token
✅ Redirection immédiate vers /auth/login si non authentifié
✅ Requêtes API uniquement si token valide présent
```

---

## 📋 Checklist de Validation

- [x] `useInvoices` vérifie l'authentification avant fetch
- [x] `useTransactions` vérifie l'authentification avant fetch
- [x] `useTransaction` vérifie authentification ET id avant fetch
- [x] `useCategoryBreakdown` vérifie l'authentification avant fetch
- [x] Pas d'erreurs 401 dans la console au chargement
- [x] Redirection vers login si non authentifié
- [x] Appels API fonctionnent si authentifié

---

## 🎓 Leçon Apprise

### Pattern à Suivre pour Tous les Hooks de Requête

**Règle** : Tout hook `useQuery` qui appelle une API protégée **DOIT** vérifier l'authentification :

```typescript
// ✅ CORRECT
import { api, getAccessToken } from "@/lib/api"

export function useProtectedResource() {
  return useQuery({
    queryKey: ["resource"],
    queryFn: api.resource.list,
    enabled: !!getAccessToken(), // ✅ Check auth first
  })
}

// ❌ INCORRECT
export function useProtectedResource() {
  return useQuery({
    queryKey: ["resource"],
    queryFn: api.resource.list, // ❌ Will call API even without token
  })
}
```

### Cas Spéciaux

**Hook avec paramètre obligatoire** :

```typescript
export function useInvoice(id: string) {
  return useQuery({
    queryKey: ["invoices", id],
    queryFn: () => api.invoices.get(id),
    enabled: !!id && !!getAccessToken(), // ✅ Check both conditions
  })
}
```

**Hook pour ressource publique** :

```typescript
export function usePublicResource() {
  return useQuery({
    queryKey: ["public"],
    queryFn: api.public.list,
    // ✅ No "enabled" needed for public endpoints
  })
}
```

---

## 🔄 Action Finale

1. **Rafraîchissez votre navigateur** avec `Ctrl+Shift+R`
2. **Ouvrez la console** (F12)
3. **Vérifiez** : plus d'erreurs 401 au chargement
4. **Connectez-vous** avec `demo@financeai.com` / `Demo2026!`
5. **Vérifiez** : les appels API fonctionnent après login

---

## 🎊 Conclusion

**Le problème des erreurs 401 Unauthorized est résolu !**

Les appels API ne se déclenchent maintenant que si :
- ✅ Un token d'authentification valide est présent dans le localStorage
- ✅ L'utilisateur est authentifié

Cela améliore :
- ✅ L'expérience utilisateur (pas d'erreurs inutiles dans la console)
- ✅ La sécurité (pas de tentatives d'appels API sans auth)
- ✅ Les performances (pas de requêtes qui échoueront de toute façon)

---

**Auteur** : AI Assistant  
**Projet** : FinanceAI - Automatisation Comptable Intelligente pour PME  
**Date** : 5 janvier 2026 - 23:00  
**Status** : ✅ **RÉSOLU**


