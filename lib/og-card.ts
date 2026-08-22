// Owns the /og route's contract in one place so the producer (metadata) and
// consumer (the route) can't drift on the param name or length limit.

// Beyond this the title overflows the card.
export const OG_TITLE_MAX_LENGTH = 120

export function ogCardUrl(title?: string): string {
  return title ? `/og?title=${encodeURIComponent(title)}` : '/og'
}

export function resolveCardTitle(param: string | null, fallback: string): string {
  const trimmed = param?.trim()
  return trimmed ? trimmed.slice(0, OG_TITLE_MAX_LENGTH) : fallback
}
