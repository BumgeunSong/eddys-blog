const NEW_BLOG_URL = 'https://www.eddysong.com'

// Points readers of the archive to the new blog and its newsletter.
export function NewBlogBanner() {
  return (
    <div className="px-4 py-2 text-center text-sm bg-gray-100 text-gray-700 dark:bg-neutral-900 dark:text-gray-300">
      이곳은 지난 글을 모아 둔 아카이브입니다. 새 글과 뉴스레터는{' '}
      <a href={NEW_BLOG_URL} className="underline underline-offset-2">
        www.eddysong.com
      </a>
      에서 읽고 구독할 수 있습니다.
    </div>
  )
}
