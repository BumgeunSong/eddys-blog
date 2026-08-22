import type { MetadataRoute } from 'next'
import { siteConfig } from '@/lib/site-config'
import { parseValidDate } from '@/lib/format-date'
import { getIndexablePosts } from './(site)/posts/get-posts'

// getIndexablePosts() drops visibility:private posts and noindex sources, so
// nothing we mark noindex is also submitted here — a page can't be both
// "please index this" and "don't index this".
// Year archives are intentionally omitted — they're noindex, so listing them
// here would contradict that signal.
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getIndexablePosts()

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
