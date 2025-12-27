import { PostItem } from '@/components/PostItem'
import { getPosts } from './posts/get-posts'

export const metadata = {
  title: '에디의 블로그'
}

export default async function HomePage() {
  const posts = await getPosts()

  return (
    <article>
      <h1>에디의 블로그</h1>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {posts.map((post) => (
          <PostItem key={post.route} post={post} />
        ))}
      </ul>
    </article>
  )
}
