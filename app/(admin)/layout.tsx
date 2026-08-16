import type { ReactNode } from 'react'

// Minimal root layout for the (admin) route group (Keystatic).
// Deliberately does NOT include the Nextra blog chrome or globals.css, so
// Keystatic renders full-width with its own styling. Provides only the
// required <html>/<body> document shell.
export const metadata = {
  title: 'Keystatic CMS',
}

export default function AdminLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  )
}
