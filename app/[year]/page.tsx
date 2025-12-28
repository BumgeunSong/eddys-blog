import { PostItem } from '@/components/PostItem'
import { YearNav } from '@/components/YearNav'
import { getAvailableYears, getPosts } from '../posts/get-posts'
import { notFound } from 'next/navigation'

export async function generateStaticParams() {
  const years = await getAvailableYears()
  const currentYear = new Date().getFullYear()

  return years
    .filter((y) => y !== currentYear)
    .map((year) => ({ year: year.toString() }))
}

export async function generateMetadata({ params }: { params: Promise<{ year: string }> }) {
  const { year } = await params
  return {
    title: `${year}년 - 에디의 블로그`
  }
}

export default async function YearPage({ params }: { params: Promise<{ year: string }> }) {
  const { year: yearParam } = await params
  const year = parseInt(yearParam, 10)

  if (isNaN(year)) {
    notFound()
  }

  const years = await getAvailableYears()

  if (!years.includes(year)) {
    notFound()
  }

  const posts = await getPosts(year)

  return (
    <article>
      <header className="mb-5 pb-3 border-b border-gray-200/15">
        <h1 className="text-3xl font-bold tracking-tight">에디의 블로그</h1>
        <YearNav years={years} currentYear={year} />
      </header>
      <div className="flex flex-col">
        {posts.map((post) => (
          <PostItem key={post.route} post={post} />
        ))}
      </div>
    </article>
  )
}
