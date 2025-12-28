import Link from 'next/link'
import type { ReactNode } from 'react'

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

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}. ${month}. ${day}`
}

export function PostLayout({ children, metadata }: PostLayoutProps) {
  const { title, date, source, tags, description } = metadata

  return (
    <article>
      <nav className="mb-4">
        <Link
          href="/"
          className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
        >
          ← 목록
        </Link>
      </nav>

      <header className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight mb-3">{title}</h1>

        {description && (
          <p className="text-base text-gray-500 dark:text-gray-400 mb-4 leading-relaxed">
            {description}
          </p>
        )}

        <div className="flex flex-wrap items-center gap-x-2 text-sm text-gray-500 dark:text-gray-400">
          {date && <span>{formatDate(date)}</span>}
          {date && source && <span>·</span>}
          {source && <span>published in {sourceLabels[source] || source}</span>}
        </div>

        {tags && tags.length > 0 && (
          <div className="mt-3 text-sm text-gray-500 dark:text-gray-400">
            {tags.join(', ')}
          </div>
        )}
      </header>

      <div className="prose-content">
        {children}
      </div>
    </article>
  )
}
