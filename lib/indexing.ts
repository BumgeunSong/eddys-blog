import type { Metadata } from 'next'

/**
 * Sources whose posts must stay out of search engines.
 *
 * These were written for a private group, so the posts stay reachable on the
 * blog — still browsable from the year archives, still linkable — but are kept
 * out of the sitemap, out of the (indexed) home listing, and marked `noindex`.
 *
 * Deliberately NOT enforced via robots.txt `Disallow`: blocking the crawl would
 * stop Google from ever seeing the `noindex`, and any inbound link would keep
 * the URL in the index as a bare title. Letting crawlers in and telling them
 * "noindex" is what actually gets an already-indexed page dropped.
 *
 * Matched against frontmatter `source` only. A post's filename is not a
 * reliable stand-in — Keystatic edits the slug and `source` independently.
 */
const NOINDEX_SOURCES = new Set(['daily-writing-friends'])

export function isNoIndexSource(source: unknown): boolean {
  return typeof source === 'string' && NOINDEX_SOURCES.has(source)
}

/**
 * `noimageindex` matters here: these posts embed photos, and without it Google
 * Images can still surface them even when the page itself is deindexed.
 */
export const NOINDEX_ROBOTS: Metadata['robots'] = {
  index: false,
  follow: false,
  nocache: true,
  googleBot: {
    index: false,
    follow: false,
    noimageindex: true
  }
}
