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
      <header className="page-header">
        <h1 className="page-title">에디의 블로그</h1>
        <YearNav years={years} currentYear={currentYear} />
      </header>
      <div className="post-list">
        {posts.map((post) => (
          <PostItem key={post.route} post={post} />
        ))}
      </div>
    </article>
  )
}
