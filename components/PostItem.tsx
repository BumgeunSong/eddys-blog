import Link from 'next/link'
import type { ReactNode } from 'react'

interface Post {
  route: string
  title: ReactNode
  frontMatter?: {
    date?: string
    description?: string
    source?: string
  }
}

export function PostItem({ post }: { post: Post }) {
  const { date, description, source } = post.frontMatter || {}

  return (
    <Link href={post.route} className="post-item">
      <div className="post-meta">
        {date && <span className="post-date">{date}</span>}
        {source && (
          <span className={`post-source ${source}`}>
            {source}
          </span>
        )}
      </div>
      <div className="post-title">{post.title}</div>
      {description && (
        <div className="post-description">{description}</div>
      )}
    </Link>
  )
}
