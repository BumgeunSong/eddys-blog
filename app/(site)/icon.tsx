import { ImageResponse } from 'next/og'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'

export const size = { width: 32, height: 32 }
export const contentType = 'image/png'

const pretendard = await readFile(
  join(process.cwd(), 'assets/Pretendard-SemiBold.otf')
)

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#18181b',
          color: '#ffffff',
          fontSize: 22,
          fontFamily: 'Pretendard'
        }}
      >
        에
      </div>
    ),
    {
      ...size,
      fonts: [
        { name: 'Pretendard', data: pretendard, style: 'normal', weight: 600 }
      ]
    }
  )
}
