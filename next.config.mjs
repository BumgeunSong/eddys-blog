import nextra from 'nextra'
import {
  NOINDEX_SLUG_PREFIXES,
  NOINDEX_HEADER_VALUE
} from './lib/indexing-sources.mjs'

const withNextra = nextra({
  latex: false,
  defaultShowCopyCode: true,
  contentDirBasePath: '/posts'
})

export default withNextra({
  reactStrictMode: true,
  async headers() {
    return [
      // Second line of defence behind the `noindex` meta tag in
      // app/(site)/posts/[...slug]/page.tsx — a header applies to responses a
      // crawler never parses as HTML.
      ...NOINDEX_SLUG_PREFIXES.map((prefix) => ({
        source: `/posts/${prefix}-:slug`,
        headers: [{ key: 'X-Robots-Tag', value: NOINDEX_HEADER_VALUE }]
      })),
      // The share-card endpoint takes the post title as a query param, so a
      // crawled /og URL would put a private title in image search. It's an
      // asset endpoint, never a search result, so noindex applies to all cards.
      // Social platforms ignore X-Robots-Tag, so link previews are unaffected.
      {
        source: '/og',
        headers: [{ key: 'X-Robots-Tag', value: 'noindex, noimageindex' }]
      }
    ]
  }
})
