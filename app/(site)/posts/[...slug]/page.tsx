import { generateStaticParamsFor, importPage } from 'nextra/pages'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'
import { useMDXComponents } from '../../../../mdx-components'
import { siteConfig } from '@/lib/site-config'
import { excerptFromMarkdown } from '@/lib/excerpt'
import { ogCardUrl } from '@/lib/og-card'
import { parseValidDate } from '@/lib/format-date'
import { isNoIndexSource, NOINDEX_ROBOTS } from '@/lib/indexing'
import type { Metadata } from 'next'
import type { ReactNode } from 'react'

export const generateStaticParams = generateStaticParamsFor('slug')

async function excerptFromBody(slug: string[]): Promise<string | undefined> {
  try {
    const raw = await readFile(
      join(process.cwd(), 'content', `${slug.join('/')}.mdx`),
      'utf8'
    )
    return excerptFromMarkdown(raw)
  } catch {
    return undefined
  }
}

export async function generateMetadata(props: {
  params: Promise<{ slug: string[] }>
}): Promise<Metadata> {
  const params = await props.params
  const { metadata } = await importPage(params.slug)
  const fm = metadata as Metadata & {
    date?: string
    description?: string
    source?: string
  }

  const route = `/posts/${params.slug.join('/')}`
  const noIndex = isNoIndexSource(fm.source)
  const title = typeof fm.title === 'string' ? fm.title : undefined
  // Fall back to a body excerpt so description-less posts don't all inherit the
  // generic site tagline from the layout.
  const description =
    fm.description?.trim() || (await excerptFromBody(params.slug))

  const publishedTime = parseValidDate(fm.date)?.toISOString()

  // Relative URL; metadataBase (root layout) makes it absolute in the tags.
  const ogImage = ogCardUrl(title ?? siteConfig.name)

  return {
    ...metadata,
    description,
    // A canonical URL asks search engines to index *this* URL, which
    // contradicts noindex. `canonical: null` is required rather than merely
    // omitting `alternates`: without it the page inherits the root layout's
    // `canonical: '/'`, telling Google these posts really live on the home page.
    // OpenGraph/Twitter tags stay either way — they drive link previews in
    // messengers, which is a different thing from being findable in search.
    ...(noIndex
      ? { robots: NOINDEX_ROBOTS, alternates: { canonical: null } }
      : { alternates: { canonical: route } }),
    openGraph: {
      type: 'article',
      url: route,
      siteName: siteConfig.name,
      locale: siteConfig.locale,
      title,
      description,
      publishedTime,
      authors: [siteConfig.author],
      images: [
        { url: ogImage, width: 1200, height: 630, alt: title ?? siteConfig.name }
      ]
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
