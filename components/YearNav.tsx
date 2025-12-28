import Link from 'next/link'

interface YearNavProps {
  years: number[]
  currentYear: number
}

export function YearNav({ years, currentYear }: YearNavProps) {
  const thisYear = new Date().getFullYear()

  return (
    <nav className="year-nav">
      {years.map((year) => (
        <Link
          key={year}
          href={year === thisYear ? '/' : `/${year}`}
          className={year === currentYear ? 'active' : ''}
        >
          {year}
        </Link>
      ))}
    </nav>
  )
}
