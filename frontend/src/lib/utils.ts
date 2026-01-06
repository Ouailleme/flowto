import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Merge Tailwind CSS classes with clsx
 * Used by shadcn/ui components
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format currency
 */
export function formatCurrency(
  amount: number,
  currency: string = "EUR",
  locale: string = "fr-FR"
): string {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
  }).format(amount)
}

/**
 * Format date
 */
export function formatDate(
  date: string | Date,
  locale: string = "fr-FR"
): string {
  const dateObj = typeof date === "string" ? new Date(date) : date
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(dateObj)
}

/**
 * Format date with time
 */
export function formatDateTime(
  date: string | Date,
  locale: string = "fr-FR"
): string {
  const dateObj = typeof date === "string" ? new Date(date) : date
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(dateObj)
}

/**
 * Truncate text
 */
export function truncate(str: string, length: number = 50): string {
  if (str.length <= length) return str
  return str.slice(0, length) + "..."
}

/**
 * Sleep utility for delays
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

/**
 * Get status color for badges (invoice, transaction, etc.)
 */
export function getStatusColor(status: string): string {
  const statusColors: Record<string, string> = {
    // Invoice statuses
    pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
    paid: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
    overdue: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
    cancelled: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
    
    // Transaction statuses
    completed: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
    pending_verification: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
    reconciled: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
    
    // General statuses
    active: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
    inactive: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
    draft: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
  }
  
  return statusColors[status.toLowerCase()] || "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
}
