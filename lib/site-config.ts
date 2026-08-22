function resolveSiteUrl(): string {
  if (process.env.NEXT_PUBLIC_SITE_URL) {
    return process.env.NEXT_PUBLIC_SITE_URL
  }
  // On Vercel preview / branch deploys, point metadata at the deployment's own
  // URL so absolute links (og:image → /og) resolve against the site you're
  // actually viewing, not production (which may not have this code yet).
  if (process.env.VERCEL_ENV !== 'production' && process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`
  }
  return 'https://www.eddysong.com'
}

// Reduce to the origin: the app has no base path, so sitemap URLs (which
// concatenate the base) and metadataBase-resolved canonicals (which use only
// the origin) must share one base — any path/query/fragment/trailing slash
// would make them diverge.
function toOrigin(url: string): string {
  try {
    return new URL(url).origin
  } catch {
    return url.replace(/\/+$/, '')
  }
}

export const siteConfig = {
  url: toOrigin(resolveSiteUrl()),
  name: '에디의 블로그',
  description: '개발과 삶에 대한 글',
  author: 'Eddy Song',
  locale: 'ko_KR'
} as const
