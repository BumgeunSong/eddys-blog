import Link from 'next/link'
import type { ReactNode } from 'react'
import { formatDate } from '@/lib/format-date'

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
      className="flex flex-col gap-1 py-3 px-2 -mx-2 rounded-md border-b border-gray-500/15 last:border-b-0 hover:bg-black/[0.04] dark:hover:bg-white/[0.05] active:scale-[0.99] transition-[background-color,transform] duration-150 ease-out origin-left"
    >
      {date && (
        <span className="text-sm text-gray-500 tabular-nums">{formatDate(date)}</span>
      )}
      <span className="text-base font-medium text-gray-900 dark:text-gray-100">
        {post.title}
      </span>
    </Link>
  )
}
