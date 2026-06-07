import { PostItem } from '@/components/PostItem'
import { YearNav } from '@/components/YearNav'
import { getAvailableYears, getHomeYear, getPosts } from './posts/get-posts'

export const metadata = {
  title: '에디의 블로그'
}

export default async function HomePage() {
  const years = await getAvailableYears()
  const activeYear = await getHomeYear()
  const posts = await getPosts(activeYear)

  return (
    <article>
      <header className="mb-5 pb-3 border-b border-black/10 dark:border-white/10">
        <h1 className="text-3xl font-bold tracking-tight">에디의 블로그</h1>
        <YearNav years={years} currentYear={activeYear} homeYear={activeYear} />
      </header>
      <div className="flex flex-col">
        {posts.map((post) => (
          <PostItem key={post.route} post={post} />
        ))}
      </div>
    </article>
  )
}
