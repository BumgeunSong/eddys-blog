import Link from 'next/link'
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
          <li key={post.route} style={{ marginBottom: '0.5rem' }}>
            <Link href={post.route}>
              <span>{post.frontMatter?.date}</span>{' '}
              <strong>{post.title}</strong>{' '}
              <span>{post.frontMatter?.description}</span>
            </Link>
          </li>
        ))}
      </ul>
    </article>
  )
}
