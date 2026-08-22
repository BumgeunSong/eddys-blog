import { PostItem } from '@/components/PostItem'
import { YearNav } from '@/components/YearNav'
import { ListScrollManager } from '@/components/ListScrollManager'
import { getAvailableYears, getHomeYear, getPosts } from '../posts/get-posts'
import { notFound } from 'next/navigation'
import type { Metadata } from 'next'

export async function generateStaticParams() {
  const years = await getAvailableYears()
  const homeYear = await getHomeYear()

  return years
    .filter((y) => y !== homeYear)
    .map((year) => ({ year: year.toString() }))
}

// ─────────────────────────────────────────────────────────────────────────
// EXERCISE: year-archive pages (e.g. /2024) are thin listing pages, so we
// keep them OUT of the search index while still letting crawlers walk through
// to the real posts.
//
// The `title` is already set (the root layout's template adds the brand, so
// this is just the year part). Your task: add a `robots` field that tells
// search engines to NOT index this page, but DO follow its links.
//
// Decision to make: index vs. follow are independent flags.
//   • index:  should this URL appear in search results?
//   • follow: may crawlers use the links on it to discover other pages?
// Think about which combination fits a thin archive page whose only job is to
// point at posts. (See Next's Metadata `robots` option.)
// ─────────────────────────────────────────────────────────────────────────
export async function generateMetadata({
  params
}: {
  params: Promise<{ year: string }>
}): Promise<Metadata> {
  const { year } = await params

  return {
    title: `${year}년`,
    // Thin listing page: keep it out of the index, but let crawlers follow
    // its links through to the actual posts.
    robots: { index: false, follow: true }
  }
}

export default async function YearPage({ params }: { params: Promise<{ year: string }> }) {
  const { year: yearParam } = await params
  const year = parseInt(yearParam, 10)

  if (isNaN(year)) {
    notFound()
  }

  const years = await getAvailableYears()
  const homeYear = await getHomeYear()

  if (!years.includes(year)) {
    notFound()
  }

  const posts = await getPosts(year)

  return (
    <article>
      <ListScrollManager />
      <header className="mb-5 pb-3 border-b border-black/10 dark:border-white/10">
        <h1 className="text-3xl font-bold tracking-tight">에디의 블로그</h1>
        <YearNav years={years} currentYear={year} homeYear={homeYear} />
      </header>
      <div className="flex flex-col">
        {posts.map((post) => (
          <PostItem key={post.route} post={post} />
        ))}
      </div>
    </article>
  )
}
