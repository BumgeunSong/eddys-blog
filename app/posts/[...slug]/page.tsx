import { generateStaticParamsFor, importPage } from 'nextra/pages'
import { useMDXComponents } from '../../../mdx-components'
import type { ReactNode } from 'react'

export const generateStaticParams = generateStaticParamsFor('slug')

export async function generateMetadata(props: { params: Promise<{ slug: string[] }> }) {
  const params = await props.params
  const { metadata } = await importPage(params.slug)
  return metadata
}

const Wrapper = useMDXComponents().wrapper as React.ComponentType<{
  toc: unknown
  metadata: unknown
  children: ReactNode
}>

export default async function Page(props: { params: Promise<{ slug: string[] }> }) {
  const params = await props.params
  const { default: MDXContent, toc, metadata } = await importPage(params.slug)

  return (
    <Wrapper toc={toc} metadata={metadata}>
      <MDXContent {...props} params={params} />
    </Wrapper>
  )
}
