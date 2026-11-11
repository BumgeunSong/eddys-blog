import { Layout, Navbar } from 'nextra-theme-blog'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import { Footer } from '@/components/Footer'
import { NewBlogBanner } from '@/components/NewBlogBanner'
import { siteConfig } from '@/lib/site-config'
import { ogCardUrl } from '@/lib/og-card'
import '../globals.css'
import type { Metadata } from 'next'
import type { ReactNode } from 'react'

// Root layout for the archive. Route groups are URL-transparent, so blog URLs
// (/, /[year], /posts/*) match the paths the old www site used.
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
        <NewBlogBanner />
        <Layout>
          <Navbar pageMap={await getPageMap()} />
          {children}
          <Footer />
        </Layout>
      </body>
    </html>
  )
}
