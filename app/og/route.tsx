import { ImageResponse } from 'next/og'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'
import { siteConfig } from '@/lib/site-config'
import { resolveCardTitle } from '@/lib/og-card'

// Standalone OG-card generator served at /og?title=<post title>.
// It lives here (not as an opengraph-image.tsx under the /posts/[...slug]
// catch-all) because Next.js forbids a route segment after a catch-all.
// Pages reference it explicitly via openGraph.images / twitter.images.

// Read the font once at module scope (Satori ships no CJK glyphs, so Korean
// titles need an explicit font). Pretendard covers Korean + Latin in one file.
const pretendard = await readFile(
  join(process.cwd(), 'assets/Pretendard-SemiBold.otf')
)

export function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const title = resolveCardTitle(searchParams.get('title'), siteConfig.name)

  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          background: '#faf9f7',
          padding: '80px',
          fontFamily: 'Pretendard'
        }}
      >
        <div
          style={{
            // Satori line-clamps long titles via the -webkit box model.
            display: '-webkit-box',
            WebkitBoxOrient: 'vertical',
            WebkitLineClamp: 4,
            overflow: 'hidden',
            fontSize: 68,
            lineHeight: 1.25,
            color: '#18181b'
          }}
        >
          {title}
        </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div
            style={{
              width: 56,
              height: 6,
              background: '#18181b',
              marginRight: 24,
              borderRadius: 3
            }}
          />
          <div style={{ fontSize: 34, color: '#52525b' }}>{siteConfig.name}</div>
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
      fonts: [
        {
          name: 'Pretendard',
          data: pretendard,
          style: 'normal',
          weight: 600
        }
      ]
    }
  )
}
