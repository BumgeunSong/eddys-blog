'use client'

import { useRouter } from 'next/navigation'

export function BackLink() {
  const router = useRouter()

  const handleClick = () => {
    const visitedList =
      typeof window !== 'undefined' &&
      sessionStorage.getItem('app:visitedList') === '1'

    if (visitedList) {
      router.back()
    } else {
      router.push('/')
    }
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors cursor-pointer bg-transparent border-0 p-0"
    >
      ← 목록
    </button>
  )
}
