import { sliceByCodePoints } from './text'

const FRONTMATTER = /^---\n[\s\S]*?\n---\n/
const FENCED_CODE = /```[\s\S]*?```/g
const INLINE_CODE = /`[^`]*`/g
const IMAGE = /!\[[^\]]*\]\([^)]*\)/g
const LINK = /\[([^\]]*)\]\([^)]*\)/g
const HTML_TAG = /<[^>]+>/g
const HEADING = /^\s{0,3}#{1,6}\s+/gm
const MD_SYMBOL = /[*_>#|-]/g
const WHITESPACE = /\s+/g

export function stripMarkdown(raw: string): string {
  return raw
    .replace(FRONTMATTER, '')
    .replace(FENCED_CODE, ' ')
    .replace(INLINE_CODE, ' ')
    .replace(IMAGE, ' ')
    .replace(LINK, '$1')
    .replace(HTML_TAG, ' ')
    .replace(HEADING, '')
    .replace(MD_SYMBOL, ' ')
    .replace(WHITESPACE, ' ')
    .trim()
}

export function excerptFromMarkdown(
  raw: string,
  maxLength = 155
): string | undefined {
  const text = stripMarkdown(raw)
  if (!text) return undefined
  const truncated = sliceByCodePoints(text, maxLength)
  return truncated === text ? text : `${truncated.trimEnd()}…`
}
