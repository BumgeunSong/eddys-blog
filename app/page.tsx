import { PostItem } from '@/components/PostItem'
import { YearNav } from '@/components/YearNav'
import { getAvailableYears, getPosts } from './posts/get-posts'

export const metadata = {
  title: '에디의 블로그'
}

export default async function HomePage() {
  const currentYear = new Date().getFullYear()
  const posts = await getPosts(currentYear)
  const years = await getAvailableYears()

  return (
    <article>
      <header className="mb-5 pb-3 border-b border-gray-200/15">
        <h1 className="text-3xl font-bold tracking-tight">에디의 블로그</h1>
        <YearNav years={years} currentYear={currentYear} />
      </header>
      <div className="flex flex-col">
        {posts.map((post) => (
          <PostItem key={post.route} post={post} />
        ))}
      </div>
    </article>
  )
}
