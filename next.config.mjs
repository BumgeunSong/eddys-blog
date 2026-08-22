import nextra from 'nextra'

const withNextra = nextra({
  latex: false,
  defaultShowCopyCode: true,
  contentDirBasePath: '/posts'
})

export default withNextra({
  reactStrictMode: true,
  // No per-post X-Robots-Tag rule here. Matching post routes by URL prefix
  // would mean treating `source` and the filename as interchangeable, and they
  // aren't: Keystatic edits them independently (content/meditation-for-
  // overthinking.mdx already has source: brunch with no prefix). A public post
  // that merely happened to be named with an excluded source's prefix would get
  // a noindex header while still sitting in the sitemap — silently deindexed.
  // The noindex signal is derived from frontmatter in generateMetadata, which
  // is correct by construction; a URL-shaped approximation of it is not worth
  // that failure mode.
  async headers() {
    return [
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
