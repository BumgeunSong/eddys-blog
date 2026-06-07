import Link from 'next/link'
import type { ReactNode } from 'react'
import { formatDate } from '@/lib/format-date'

interface PostMetadata {
  title?: string
  date?: string
  source?: string
  tags?: string[]
  description?: string
}

interface PostLayoutProps {
  children: ReactNode
  metadata: PostMetadata
}

const sourceLabels: Record<string, string> = {
  apple_notes: 'Apple Notes',
  'daily-writing-friends': '1일1글',
  instagram: 'Instagram',
  brunch: 'Brunch',
  learning_man: '러닝맨',
  velog: 'Velog'
}

export function PostLayout({ children, metadata }: PostLayoutProps) {
  const { title, date, source, tags, description } = metadata

  return (
    <article>
      <nav className="mb-4">
        <Link
          href="/"
          className="inline-block text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 active:-translate-x-0.5 transition-[color,transform] duration-150 ease-out"
        >
          ← 목록
        </Link>
      </nav>

      <header className="mb-6">
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-3 leading-tight">{title}</h1>

        {description && (
          <p className="text-base text-gray-500 dark:text-gray-400 mb-4 leading-relaxed">
            {description}
          </p>
        )}

        <div className="flex flex-wrap items-center gap-x-2 text-sm text-gray-500 dark:text-gray-400">
          {date && <span>{formatDate(date)}</span>}
          {date && source && <span>·</span>}
          {source && <span>{sourceLabels[source] || source}에 발행</span>}
        </div>

        {tags && tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {tags.map((tag) => (
              <span
                key={tag}
                className="rounded-full bg-black/[0.05] dark:bg-white/[0.07] px-2.5 py-1 text-xs text-gray-600 dark:text-gray-300"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </header>

      <div className="prose-content">
        {children}
      </div>
    </article>
  )
}
