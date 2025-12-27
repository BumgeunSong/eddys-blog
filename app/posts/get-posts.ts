import { normalizePages } from 'nextra/normalize-pages'
import { getPageMap } from 'nextra/page-map'

export async function getPosts() {
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

export async function getTags(): Promise<string[]> {
  const posts = await getPosts()
  const tags = posts.flatMap((post) => post.frontMatter?.tags || [])
  return [...new Set(tags)]
}
