import type { MetadataRoute } from 'next'
import { siteConfig } from '@/lib/site-config'
import { getPosts } from './(site)/posts/get-posts'

// Auto-generated at /sitemap.xml. Reuses getPosts(), which already excludes
// visibility:private posts, so nothing private is ever exposed to crawlers.
// Year-archive pages are intentionally omitted: they are noindex thin listing
// pages, so advertising them here would contradict that signal.
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getPosts()

  const now = new Date()

  const postEntries: MetadataRoute.Sitemap = posts.map((post) => {
    const date = post.frontMatter?.date
      ? new Date(post.frontMatter.date)
      : undefined
    const hasValidDate = date && !Number.isNaN(date.getTime())
    // Omit lastModified when there's no real date, so date-less posts don't
    // look freshly updated on every build.
    return {
      url: `${siteConfig.url}${post.route}`,
      ...(hasValidDate ? { lastModified: date } : {})
    }
  })

  return [{ url: siteConfig.url, lastModified: now }, ...postEntries]
}
