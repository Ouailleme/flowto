import axios, { AxiosError, AxiosRequestConfig } from "axios"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Create axios instance
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
})

// Request interceptor - Add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & {
      _retry?: boolean
    }

    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // TODO: Implement token refresh
        // const newToken = await refreshAccessToken()
        // if (newToken) {
        //   originalRequest.headers.Authorization = `Bearer ${newToken}`
        //   return apiClient(originalRequest)
        // }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        clearAuth()
        if (typeof window !== "undefined") {
          window.location.href = "/auth/login"
        }
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Auth helpers
export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem("access_token")
}

export function setAccessToken(token: string): void {
  if (typeof window === "undefined") return
  localStorage.setItem("access_token", token)
}

export function clearAuth(): void {
  if (typeof window === "undefined") return
  localStorage.removeItem("access_token")
  localStorage.removeItem("refresh_token")
  localStorage.removeItem("user")
}

// API Error type
export interface APIError {
  detail: string
  status_code?: number
}

// Generic API call wrapper
export async function apiCall<T>(
  config: AxiosRequestConfig
): Promise<T> {
  try {
    const response = await apiClient(config)
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const apiError: APIError = {
        detail: error.response?.data?.detail || error.message,
        status_code: error.response?.status,
      }
      throw apiError
    }
    throw error
  }
}

// API endpoints
export const api = {
  // Auth
  auth: {
    login: (email: string, password: string) =>
      apiCall<{ access_token: string; token_type: string }>({
        method: "POST",
        url: "/api/v1/auth/login",
        data: { email, password },
      }),
    register: (data: { email: string; password: string; full_name?: string }) =>
      apiCall<{ id: string; email: string }>({
        method: "POST",
        url: "/api/v1/auth/register",
        data,
      }),
    me: () =>
      apiCall<{
        id: string
        email: string
        full_name?: string
        is_active: boolean
      }>({
        method: "GET",
        url: "/api/v1/auth/me",
      }),
  },

  // Banks
  banks: {
    list: () =>
      apiCall<{ accounts: any[]; total: number }>({
        method: "GET",
        url: "/api/v1/banks/",
      }),
    create: (data: any) =>
      apiCall({
        method: "POST",
        url: "/api/v1/banks/",
        data,
      }),
  },

  // Transactions
  transactions: {
    list: (params?: any) =>
      apiCall<{
        transactions: any[]
        total: number
        page: number
        page_size: number
        total_pages: number
      }>({
        method: "GET",
        url: "/api/v1/transactions/",
        params,
      }),
    get: (id: string) =>
      apiCall({
        method: "GET",
        url: `/api/v1/transactions/${id}/`,
      }),
  },

  // Invoices
  invoices: {
    list: (params?: any) =>
      apiCall<{
        invoices: any[]
        total: number
        page: number
        page_size: number
        total_pages: number
      }>({
        method: "GET",
        url: "/api/v1/invoices/",
        params,
      }),
    create: (data: any) =>
      apiCall({
        method: "POST",
        url: "/api/v1/invoices/",
        data,
      }),
    update: (id: string, data: any) =>
      apiCall({
        method: "PATCH",
        url: `/api/v1/invoices/${id}/`,
        data,
      }),
    delete: (id: string) =>
      apiCall({
        method: "DELETE",
        url: `/api/v1/invoices/${id}/`,
      }),
  },

  // Reconciliations
  reconciliations: {
    create: (data: any) =>
      apiCall({
        method: "POST",
        url: "/api/v1/reconciliations/",
        data,
      }),
    suggestions: (transactionId: string) =>
      apiCall<any[]>({
        method: "GET",
        url: `/api/v1/reconciliations/suggestions/${transactionId}/`,
      }),
    stats: () =>
      apiCall({
        method: "GET",
        url: "/api/v1/reconciliations/stats/",
      }),
  },

  // Categorization
  categorization: {
    categorize: (transactionId: string) =>
      apiCall({
        method: "POST",
        url: `/api/v1/categorization/transactions/${transactionId}/`,
      }),
    bulk: (limit?: number) =>
      apiCall<{ categorized: number }>({
        method: "POST",
        url: "/api/v1/categorization/bulk/",
        params: { limit },
      }),
    breakdown: () =>
      apiCall<Record<string, number>>({
        method: "GET",
        url: "/api/v1/categorization/breakdown/",
      }),
  },

  // Reminders
  reminders: {
    send: (invoiceId: string, reminderType: string) =>
      apiCall({
        method: "POST",
        url: `/api/v1/reminders/invoices/${invoiceId}/send/`,
        params: { reminder_type: reminderType },
      }),
    processOverdue: () =>
      apiCall<{ total: number; sent: number; failed: number }>({
        method: "POST",
        url: "/api/v1/reminders/process-overdue/",
      }),
    stats: () =>
      apiCall({
        method: "GET",
        url: "/api/v1/reminders/stats/",
      }),
  },
}

