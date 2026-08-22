import { normalizePages } from 'nextra/normalize-pages'
import { getPageMap } from 'nextra/page-map'
import { isNoIndexSource } from '@/lib/indexing'

/** How many posts the home page shows. Home spans years, so it needs a cap. */
export const HOME_POST_LIMIT = 30

async function getAllPosts() {
  const pageMap = await getPageMap('/posts')

  if (!pageMap || pageMap.length === 0) {
    return []
  }

  const { directories = [] } = normalizePages({
    list: pageMap,
    route: '/posts'
  })

  return directories
    .filter((post) => post.name !== 'index')
    .filter((post) => post.frontMatter?.visibility !== 'private')
    .sort((a, b) => {
      const dateA = new Date(a.frontMatter?.date || 0)
      const dateB = new Date(b.frontMatter?.date || 0)
      return dateB.getTime() - dateA.getTime()
    })
}

export async function getPosts(year?: number) {
  const allPosts = await getAllPosts()

  if (!year) {
    return allPosts
  }

  return allPosts.filter((post) => {
    const postDate = new Date(post.frontMatter?.date || 0)
    return postDate.getFullYear() === year
  })
}

/**
 * Posts that may be exposed to search engines — feeds the home listing and the
 * sitemap, the two surfaces crawlers actually read.
 *
 * Year archives deliberately do NOT use this: they're `noindex`, so they stay
 * complete and remain the way a visitor browses the excluded posts.
 */
export async function getIndexablePosts(limit?: number) {
  const posts = (await getAllPosts()).filter(
    (post) => !isNoIndexSource(post.frontMatter?.source)
  )

  return limit === undefined ? posts : posts.slice(0, limit)
}

export async function getAvailableYears(): Promise<number[]> {
  const allPosts = await getAllPosts()

  const years = new Set<number>()
  for (const post of allPosts) {
    const postDate = new Date(post.frontMatter?.date || 0)
    const year = postDate.getFullYear()
    if (year > 1970) {
      years.add(year)
    }
  }

  return Array.from(years).sort((a, b) => b - a)
}
