'use client'

import Link from 'next/link'
import type { ReactNode } from 'react'
import { formatDate } from '@/lib/format-date'
import { scrollKey } from './ListScrollManager'

interface Post {
  route: string
  title: ReactNode
  frontMatter?: {
    date?: string
  }
}

function saveListScroll() {
  sessionStorage.setItem(scrollKey(window.location.pathname), String(window.scrollY))
}

export function PostItem({ post }: { post: Post }) {
  const { date } = post.frontMatter || {}

  return (
    <Link
      href={post.route}
      onClick={saveListScroll}
      className="post-item-stagger flex flex-col gap-1 py-3 px-2 -mx-2 rounded-md border-b border-gray-500/15 last:border-b-0 hover:bg-black/[0.04] dark:hover:bg-white/[0.05] motion-safe:active:scale-[0.99] transition-[background-color,transform] duration-150 ease-out origin-left"
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
