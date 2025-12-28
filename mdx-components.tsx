import { useMDXComponents as getDocsMDXComponents } from 'nextra-theme-blog'
import { PostLayout } from '@/components/PostLayout'
import type { MDXComponents } from 'mdx/types'
import type { ReactNode } from 'react'

const docsComponents = getDocsMDXComponents()

interface WrapperProps {
  children: ReactNode
  metadata?: {
    title?: string
    date?: string
    source?: string
    tags?: string[]
    description?: string
    visibility?: 'public' | 'private'
  }
}

export function useMDXComponents(components?: MDXComponents): MDXComponents {
  return {
    ...docsComponents,
    wrapper: ({ children, metadata }: WrapperProps) => (
      <PostLayout metadata={metadata || {}}>{children}</PostLayout>
    ),
    ...components
  }
}
