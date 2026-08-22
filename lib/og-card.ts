// The contract for the generated OG-card route (app/og/route.tsx), owned in one
// place so the producer (page/layout metadata) and the consumer (the route)
// can't drift apart on the query-param name or length limit.

/** Longest title the card renders before it would overflow; also guards the route. */
export const OG_TITLE_MAX_LENGTH = 120

/** Build the /og image URL for a title, or the default card when omitted. */
export function ogCardUrl(title?: string): string {
  return title ? `/og?title=${encodeURIComponent(title)}` : '/og'
}

/** Resolve the title to render from the route's raw `title` query param. */
export function resolveCardTitle(param: string | null, fallback: string): string {
  const trimmed = param?.trim()
  return trimmed ? trimmed.slice(0, OG_TITLE_MAX_LENGTH) : fallback
}
