import Link from 'next/link'
import type { ReactNode } from 'react'

interface Post {
  route: string
  title: ReactNode
  frontMatter?: {
    date?: string
    description?: string
  }
}

export function PostItem({ post }: { post: Post }) {
  return (
    <li style={{ marginBottom: '0.5rem' }}>
      <Link href={post.route}>
        <span>{post.frontMatter?.date}</span>{' '}
        <strong>{post.title}</strong>{' '}
        <span>{post.frontMatter?.description}</span>
      </Link>
    </li>
  )
}
