// Pure text helpers for deriving a plain-text excerpt from raw MDX source.
// No I/O here — callers read the file and pass the string in — so these stay
// trivially unit-testable.

/** Strip frontmatter, code, and Markdown syntax down to plain prose. */
export function stripMarkdown(raw: string): string {
  return raw
    .replace(/^---\n[\s\S]*?\n---\n/, '') // drop frontmatter
    .replace(/```[\s\S]*?```/g, ' ') // fenced code
    .replace(/`[^`]*`/g, ' ') // inline code
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ') // images
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1') // links → text
    .replace(/<[^>]+>/g, ' ') // html tags
    .replace(/^\s{0,3}#{1,6}\s+/gm, '') // headings
    .replace(/[*_>#|-]/g, ' ') // leftover md symbols
    .replace(/\s+/g, ' ') // collapse whitespace
    .trim()
}

/**
 * Plain-text excerpt from raw MDX source, truncated to `maxLength` with an
 * ellipsis. Returns undefined when there's no usable text.
 */
export function excerptFromMarkdown(
  raw: string,
  maxLength = 155
): string | undefined {
  const text = stripMarkdown(raw)
  if (!text) return undefined
  return text.length > maxLength
    ? `${text.slice(0, maxLength).trimEnd()}…`
    : text
}
