import { PostItem } from '@/components/PostItem'
import { getPosts } from './posts/get-posts'

export const metadata = {
  title: '에디의 블로그'
}

export default async function HomePage() {
  const posts = await getPosts()

  return (
    <article>
      <header className="page-header">
        <h1 className="page-title">에디의 블로그</h1>
      </header>
      <div className="post-list">
        {posts.map((post) => (
          <PostItem key={post.route} post={post} />
        ))}
      </div>
    </article>
  )
}
