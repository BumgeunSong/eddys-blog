import type { MetadataRoute } from 'next'
import { siteConfig } from '@/lib/site-config'
import { parseValidDate } from '@/lib/format-date'
import { getPosts } from './(site)/posts/get-posts'

// Auto-generated at /sitemap.xml. Reuses getPosts(), which already excludes
// visibility:private posts, so nothing private is ever exposed to crawlers.
// Year-archive pages are intentionally omitted: they are noindex thin listing
// pages, so advertising them here would contradict that signal.
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getPosts()

  const now = new Date()

  const postEntries: MetadataRoute.Sitemap = posts.map((post) => {
    // Omit lastModified when there's no real date, so date-less posts don't
    // look freshly updated on every build.
    const date = parseValidDate(post.frontMatter?.date)
    return {
      url: `${siteConfig.url}${post.route}`,
      ...(date ? { lastModified: date } : {})
    }
  })

  return [{ url: siteConfig.url, lastModified: now }, ...postEntries]
}
