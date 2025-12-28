import Link from 'next/link'
import type { ReactNode } from 'react'

interface Post {
  route: string
  title: ReactNode
  frontMatter?: {
    date?: string
  }
}

export function PostItem({ post }: { post: Post }) {
  const { date } = post.frontMatter || {}

  return (
    <Link href={post.route} className="post-item">
      {date && <span className="post-date">{date}</span>}
      <span className="post-title">{post.title}</span>
    </Link>
  )
}
