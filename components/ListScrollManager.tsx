'use client'

import { useEffect } from 'react'
import { usePathname } from 'next/navigation'

export const VISITED_FLAG = 'app:visitedList'
export const scrollKey = (path: string) => `app:scroll:${path}`

export function ListScrollManager() {
  const pathname = usePathname()

  useEffect(() => {
    sessionStorage.setItem(VISITED_FLAG, '1')

    if ('scrollRestoration' in history) {
      history.scrollRestoration = 'manual'
    }

    const saved = sessionStorage.getItem(scrollKey(pathname))
    if (saved) {
      const y = parseInt(saved, 10)
      if (!Number.isNaN(y)) {
        requestAnimationFrame(() => window.scrollTo(0, y))
      }
    }
  }, [pathname])

  return null
}
