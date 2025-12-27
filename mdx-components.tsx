import { useMDXComponents as getDocsMDXComponents } from 'nextra-theme-blog'
import type { MDXComponents } from 'mdx/types'

const docsComponents = getDocsMDXComponents()

export function useMDXComponents(components?: MDXComponents): MDXComponents {
  return {
    ...docsComponents,
    ...components
  }
}
