import { normalizePages } from 'nextra/normalize-pages'
import { getPageMap } from 'nextra/page-map'

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
