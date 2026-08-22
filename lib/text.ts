// Slice by Unicode code points, not UTF-16 units, so truncation never splits an
// emoji surrogate pair into a replacement glyph.
export function sliceByCodePoints(text: string, max: number): string {
  return Array.from(text).slice(0, max).join('')
}
