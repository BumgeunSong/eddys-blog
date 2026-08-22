/**
 * Single source of truth for "which posts must stay out of search engines".
 *
 * Plain .mjs (not .ts) because next.config.mjs imports it at config load time,
 * where TypeScript is not available. lib/indexing.ts re-exports these and adds
 * the typed Next.js Metadata helpers on top.
 *
 * Named `indexing-sources` rather than `indexing` on purpose: webpack resolves
 * `.mjs` before `.ts`, so a sibling `lib/indexing.mjs` would silently shadow
 * `lib/indexing.ts` for every `@/lib/indexing` import.
 */

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
 */
export const NOINDEX_SOURCES = ['daily-writing-friends']

/** Content files are named `{source}-{id}.mdx`, so the source doubles as a route prefix. */
export const NOINDEX_SLUG_PREFIXES = NOINDEX_SOURCES

export const NOINDEX_HEADER_VALUE = 'noindex, nofollow, noimageindex, noarchive'
