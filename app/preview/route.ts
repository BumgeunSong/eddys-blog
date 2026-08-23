import { redirect } from 'next/navigation'

const PREVIEW_DEPLOY_URL =
  process.env.PREVIEW_DEPLOY_URL ??
  'https://writing-archiver-git-{branch}-bumgeunsongs-projects.vercel.app'

// A DNS label maxes out at 63 chars; beyond that Vercel truncates the branch and
// appends a hash we can't reproduce, so the host 404s.
const MAX_SUBDOMAIN_LABEL = 63

function branchToOrigin(branch: string, origin: string): string {
  // `main` is production (no separate branch deployment). Compare the RAW ref so
  // case-distinct branches like "MAIN" aren't collapsed onto production below.
  if (branch === 'main') {
    return origin
  }

  // Mirror Vercel's branch → subdomain transform.
  const safe = branch
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')

  if (!safe) {
    return origin
  }

  return PREVIEW_DEPLOY_URL.replace('{branch}', safe)
}

export async function GET(req: Request) {
  const { searchParams, origin } = new URL(req.url)
  const branch = searchParams.get('branch')
  const to = searchParams.get('to') ?? '/'

  if (!branch) {
    return new Response('Missing "branch" query param', { status: 400 })
  }

  const base = new URL(branchToOrigin(branch, origin))

  if (base.hostname.split('.')[0].length > MAX_SUBDOMAIN_LABEL) {
    return new Response(
      'Branch name is too long for a Vercel preview subdomain — use a shorter branch name.',
      { status: 400 },
    )
  }

  // Guard against open redirects: `to` is request-controlled, so reject absolute
  // or protocol-relative targets that would resolve off `base`'s origin. `new URL`
  // also throws on malformed input (e.g. "http://["), which must be a 400, not a 500.
  let target: URL
  try {
    target = new URL(to, base)
  } catch {
    return new Response('Invalid "to" target.', { status: 400 })
  }
  if (target.origin !== base.origin) {
    return new Response('Invalid "to" target — must be a path on the preview origin.', {
      status: 400,
    })
  }

  redirect(target.toString())
}
