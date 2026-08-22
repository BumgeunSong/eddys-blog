import { PostItem } from '@/components/PostItem'
import { YearNav } from '@/components/YearNav'
import { ListScrollManager } from '@/components/ListScrollManager'
import { getAvailableYears, getIndexablePosts, HOME_POST_LIMIT } from './posts/get-posts'

export const metadata = {
  title: '에디의 블로그'
}

// The home page is indexed, so it lists only indexable posts — a noindex post's
// title must not reach search results via this listing. That makes home a
// "recent posts" view spanning years rather than a single-year archive; the
// full per-year archives (noindex) are how visitors browse the excluded posts.
export default async function HomePage() {
  const years = await getAvailableYears()
  const posts = await getIndexablePosts(HOME_POST_LIMIT)

  return (
    <article>
      <ListScrollManager />
      <header className="mb-5 pb-3 border-b border-black/10 dark:border-white/10">
        <h1 className="text-3xl font-bold tracking-tight">에디의 블로그</h1>
        <YearNav years={years} />
      </header>
      <div className="flex flex-col">
        {posts.map((post) => (
          <PostItem key={post.route} post={post} />
        ))}
      </div>
    </article>
  )
}
