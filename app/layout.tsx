import { Layout, Navbar } from 'nextra-theme-blog'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import { Footer } from '@/components/Footer'
import './globals.css'
import type { ReactNode } from 'react'

export const metadata = {
  title: "에디의 블로그",
  description: "개발과 삶에 대한 글"
}

export default async function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <Head />
      <body>
        <Layout>
          <Navbar pageMap={await getPageMap()} />
          {children}
          <Footer />
        </Layout>
      </body>
    </html>
  )
}
