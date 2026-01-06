/**
 * Frontend monitoring with Sentry.
 * Captures errors and performance metrics.
 */

declare global {
  interface Window {
    Sentry?: any;
  }
}

/**
 * Initialize Sentry for error tracking.
 * Call this early in your app initialization.
 */
export function initSentry() {
  const sentryDsn = process.env.NEXT_PUBLIC_SENTRY_DSN;
  const environment = process.env.NEXT_PUBLIC_ENVIRONMENT || "development";
  const version = process.env.NEXT_PUBLIC_VERSION || "0.1.0";

  if (!sentryDsn) {
    console.info("Sentry DSN not configured. Skipping Sentry initialization.");
    return;
  }

  // Check if Sentry SDK is available
  if (typeof window === "undefined" || !window.Sentry) {
    console.warn(
      "Sentry SDK not loaded. Install with: npm install @sentry/nextjs"
    );
    return;
  }

  try {
    window.Sentry.init({
      dsn: sentryDsn,
      environment,
      release: `flowto-frontend@${version}`,

      // Performance monitoring
      tracesSampleRate: 0.1, // 10% of transactions
      replaysSessionSampleRate: 0.1, // 10% of sessions
      replaysOnErrorSampleRate: 1.0, // 100% of sessions with errors

      // Integrations
      integrations: [
        new window.Sentry.BrowserTracing({
          // Trace HTTP requests
          tracePropagationTargets: [
            "localhost",
            /^https:\/\/api\.flowto\.fr/,
          ],
        }),
        new window.Sentry.Replay({
          maskAllText: true, // Mask all text for privacy
          blockAllMedia: true, // Block all media for privacy
        }),
      ],

      // Filter sensitive data
      beforeSend(event, hint) {
        // Remove sensitive data from breadcrumbs
        if (event.breadcrumbs) {
          event.breadcrumbs = event.breadcrumbs.map((breadcrumb) => {
            if (breadcrumb.data) {
              // Remove passwords, tokens, etc.
              const sensitiveKeys = [
                "password",
                "token",
                "apiKey",
                "secret",
                "authorization",
              ];
              sensitiveKeys.forEach((key) => {
                if (key in breadcrumb.data!) {
                  breadcrumb.data![key] = "[Filtered]";
                }
              });
            }
            return breadcrumb;
          });
        }

        // Remove sensitive data from extra context
        if (event.extra) {
          const sensitiveKeys = ["password", "token", "apiKey", "secret"];
          sensitiveKeys.forEach((key) => {
            if (key in event.extra!) {
              event.extra![key] = "[Filtered]";
            }
          });
        }

        return event;
      },
    });

    console.info(`Sentry initialized for environment: ${environment}`);
  } catch (error) {
    console.error("Failed to initialize Sentry:", error);
  }
}

/**
 * Capture an exception in Sentry.
 */
export function captureException(error: Error, context?: Record<string, any>) {
  if (typeof window !== "undefined" && window.Sentry) {
    if (context) {
      window.Sentry.setContext("error_context", context);
    }
    window.Sentry.captureException(error);
  } else {
    console.error("Sentry not initialized:", error);
  }
}

/**
 * Set user context in Sentry.
 */
export function setUser(user: { id: string; email?: string } | null) {
  if (typeof window !== "undefined" && window.Sentry) {
    if (user) {
      window.Sentry.setUser({
        id: user.id,
        email: user.email,
      });
    } else {
      window.Sentry.setUser(null);
    }
  }
}

/**
 * Add breadcrumb for tracking user actions.
 */
export function addBreadcrumb(
  message: string,
  category: string,
  level: "info" | "warning" | "error" = "info",
  data?: Record<string, any>
) {
  if (typeof window !== "undefined" && window.Sentry) {
    window.Sentry.addBreadcrumb({
      message,
      category,
      level,
      data,
    });
  }
}

