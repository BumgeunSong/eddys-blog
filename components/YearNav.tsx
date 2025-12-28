import Link from 'next/link'

interface YearNavProps {
  years: number[]
  currentYear: number
}

export function YearNav({ years, currentYear }: YearNavProps) {
  const thisYear = new Date().getFullYear()

  return (
    <nav className="flex gap-4 mt-3 flex-wrap">
      {years.map((year) => (
        <Link
          key={year}
          href={year === thisYear ? '/' : `/${year}`}
          className={`text-sm py-1 hover:opacity-70 transition-opacity ${
            year === currentYear
              ? 'font-semibold text-gray-900 dark:text-gray-100'
              : 'text-gray-500 dark:text-gray-400'
          }`}
        >
          {year}
        </Link>
      ))}
    </nav>
  )
}
