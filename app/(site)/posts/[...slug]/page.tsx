import { generateStaticParamsFor, importPage } from 'nextra/pages'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'
import { useMDXComponents } from '../../../../mdx-components'
import { siteConfig } from '@/lib/site-config'
import { excerptFromMarkdown } from '@/lib/excerpt'
import { ogCardUrl } from '@/lib/og-card'
import { parseValidDate } from '@/lib/format-date'
import type { Metadata } from 'next'
import type { ReactNode } from 'react'

export const generateStaticParams = generateStaticParamsFor('slug')

// Read a post's raw MDX and derive a plain-text excerpt (used as a description
// fallback for posts without frontmatter). I/O only — the text work is pure.
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
  const fm = metadata as Metadata & { date?: string; description?: string }

  const route = `/posts/${params.slug.join('/')}`
  const title = typeof fm.title === 'string' ? fm.title : undefined
  // Prefer the author's frontmatter description; otherwise derive one from the
  // body so description-less posts get a unique snippet instead of the generic
  // site tagline inherited from the layout.
  const description =
    fm.description?.trim() || (await excerptFromBody(params.slug))

  // Only emit a valid ISO publishedTime; skip if the frontmatter date is missing/bad.
  const publishedTime = parseValidDate(fm.date)?.toISOString()

  // Branded share card generated on demand by /og; metadataBase (set in the
  // root layout) resolves this relative URL to an absolute one for the tags.
  const ogImage = ogCardUrl(title ?? siteConfig.name)

  return {
    ...metadata,
    description,
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
