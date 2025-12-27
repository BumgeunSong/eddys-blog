import Link from 'next/link'
import { PostCard } from 'nextra-theme-blog'
import { getPosts, getTags } from './get-posts'

export const metadata = {
  title: '글 목록 - 에디의 블로그'
}

export default async function PostsPage() {
  const posts = await getPosts()
  const tags = await getTags()

  return (
    <article>
      <h1>글 목록</h1>

      {tags.length > 0 && (
        <div style={{ marginBottom: '2rem' }}>
          {tags.map((tag) => (
            <Link
              key={tag}
              href={`/tags/${tag}`}
              style={{
                marginRight: '0.5rem',
                padding: '0.25rem 0.5rem',
                backgroundColor: 'var(--nextra-primary-hue)',
                borderRadius: '0.25rem',
                fontSize: '0.875rem'
              }}
            >
              #{tag}
            </Link>
          ))}
        </div>
      )}

      <div>
        {posts.map((post) => (
          <PostCard key={post.route} post={post} />
        ))}
      </div>
    </article>
  )
}
