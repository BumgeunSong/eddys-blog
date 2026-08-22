import { Layout, Navbar } from 'nextra-theme-blog'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import { Footer } from '@/components/Footer'
import { siteConfig } from '@/lib/site-config'
import { ogCardUrl } from '@/lib/og-card'
import '../globals.css'
import type { Metadata } from 'next'
import type { ReactNode } from 'react'

// Root layout for the public blog. Lives in the (site) route group so the
// Keystatic admin (in the (admin) group) does NOT inherit the Nextra blog
// chrome / narrow article container. Route groups are URL-transparent, so
// blog URLs (/, /[year], /posts/*) are unchanged.
export const metadata: Metadata = {
  // Lets child pages use relative OG/canonical URLs (resolved to absolute here).
  metadataBase: new URL(siteConfig.url),
  title: {
    default: siteConfig.name,
    template: `%s – ${siteConfig.name}`
  },
  description: siteConfig.description,
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    locale: siteConfig.locale,
    url: siteConfig.url,
    siteName: siteConfig.name,
    title: siteConfig.name,
    description: siteConfig.description,
    images: [{ url: ogCardUrl(), width: 1200, height: 630, alt: siteConfig.name }]
  },
  twitter: {
    card: 'summary_large_image',
    title: siteConfig.name,
    description: siteConfig.description,
    images: [ogCardUrl()]
  }
}

export default async function SiteLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <Head />
      <body>
        <Layout>
          <Navbar pageMap={await getPageMap()} />
          {children}
          <Footer />
        </Layout>
      </body>
    </html>
  )
}
