import type { MetadataRoute } from 'next'
import { siteConfig } from '@/lib/site-config'
import { parseValidDate } from '@/lib/format-date'
import { getPosts } from './(site)/posts/get-posts'

// getPosts() excludes visibility:private posts, so nothing private is exposed.
// Year archives are intentionally omitted — they're noindex, so listing them
// here would contradict that signal.
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
