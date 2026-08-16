import { generateStaticParamsFor, importPage } from 'nextra/pages'
import { useMDXComponents } from '../../../../mdx-components'
import { siteConfig } from '@/lib/site-config'
import type { Metadata } from 'next'
import type { ReactNode } from 'react'

export const generateStaticParams = generateStaticParamsFor('slug')

export async function generateMetadata(props: {
  params: Promise<{ slug: string[] }>
}): Promise<Metadata> {
  const params = await props.params
  const { metadata } = await importPage(params.slug)
  const fm = metadata as Metadata & { date?: string; description?: string }

  const route = `/posts/${params.slug.join('/')}`
  const title = typeof fm.title === 'string' ? fm.title : undefined
  const description = fm.description

  // Only emit a valid ISO publishedTime; skip if the frontmatter date is missing/bad.
  const published = fm.date ? new Date(fm.date) : undefined
  const publishedTime =
    published && !Number.isNaN(published.getTime())
      ? published.toISOString()
      : undefined

  // Branded share card generated on demand by /og; metadataBase (set in the
  // root layout) resolves this relative URL to an absolute one for the tags.
  const ogImage = `/og?title=${encodeURIComponent(title ?? siteConfig.name)}`

  return {
    ...metadata,
    alternates: { canonical: route },
    openGraph: {
      type: 'article',
      url: route,
      siteName: siteConfig.name,
      locale: siteConfig.locale,
      title,
      description,
      publishedTime,
      authors: [siteConfig.author],
      images: [{ url: ogImage, width: 1200, height: 630, alt: title }]
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: [ogImage]
    }
  }
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
