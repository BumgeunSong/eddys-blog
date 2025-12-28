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
    <Link
      href={post.route}
      className="flex flex-col gap-1 py-3 border-b border-gray-500/15 hover:opacity-60 transition-opacity last:border-b-0"
    >
      {date && (
        <span className="text-sm text-gray-500 tabular-nums">{date}</span>
      )}
      <span className="text-base font-medium text-gray-900 dark:text-gray-100">
        {post.title}
      </span>
    </Link>
  )
}
