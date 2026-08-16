// Single source of truth for site-wide SEO / social metadata.
// Override the URL per-environment with NEXT_PUBLIC_SITE_URL (e.g. preview deploys);
// falls back to the production domain used in keystatic.config.ts.
export const siteConfig = {
  url: process.env.NEXT_PUBLIC_SITE_URL ?? 'https://www.eddysong.com',
  name: '에디의 블로그',
  description: '개발과 삶에 대한 글',
  author: 'Eddy Song',
  locale: 'ko_KR'
} as const
