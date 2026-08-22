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
    return {
      url: `${siteConfig.url}${post.route}`,
      lastModified:
        date && !Number.isNaN(date.getTime()) ? date : now
    }
  })

  return [{ url: siteConfig.url, lastModified: now }, ...postEntries]
}
