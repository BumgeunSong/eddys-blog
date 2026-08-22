import { NOINDEX_SOURCES } from './indexing-sources.mjs'
import type { Metadata } from 'next'

export {
  NOINDEX_SOURCES,
  NOINDEX_SLUG_PREFIXES,
  NOINDEX_HEADER_VALUE
} from './indexing-sources.mjs'

const noIndexSources = new Set<string>(NOINDEX_SOURCES)

export function isNoIndexSource(source: unknown): boolean {
  return typeof source === 'string' && noIndexSources.has(source)
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
