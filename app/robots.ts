import type { MetadataRoute } from 'next'
import { siteConfig } from '@/lib/site-config'

// Auto-generated at /robots.txt. Allows all content, keeps crawlers out of the
// Keystatic admin + API routes, and advertises the sitemap.
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/keystatic', '/api/']
    },
    sitemap: `${siteConfig.url}/sitemap.xml`
  }
}
