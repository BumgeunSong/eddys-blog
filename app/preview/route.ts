import { redirect } from 'next/navigation'

// Vercel serves every git branch at a deterministic "branch alias" host:
//   {project}-git-{branch}-{scope}.vercel.app
// For this project/scope the fixed part is 43 chars, and a single subdomain
// label maxes out at 63 chars — so keep branch names under ~20 chars. Beyond
// that Vercel truncates the branch and appends a hash we can't reproduce here.
// The {branch} placeholder is substituted at runtime by branchToOrigin().
const PREVIEW_DEPLOY_URL =
  process.env.PREVIEW_DEPLOY_URL ??
  'https://writing-archiver-git-{branch}-bumgeunsongs-projects.vercel.app'

/**
 * Resolve the origin that will render a draft for `branch`.
 *
 * Two cases to handle:
 *   1. `main` IS production — there is no separate "main" branch deployment, so
 *      return `origin` (this very site) and the preview just opens the live page.
 *   2. Any other branch → its Vercel branch-alias host. Vercel lowercases the
 *      branch and replaces every run of non-alphanumeric characters (notably
 *      "/") with a single "-". Reproduce that, then substitute it into
 *      PREVIEW_DEPLOY_URL's {branch} slot.
 *
 * @param branch raw branch name from Keystatic (may be "main", "Feature/Foo", …)
 * @param origin origin this route is served from (production)
 * @returns absolute origin, e.g. "https://writing-archiver-git-my-draft-bumgeunsongs-projects.vercel.app"
 */
function branchToOrigin(branch: string, origin: string): string {
  // Mirror Vercel's branch → subdomain transform: lowercase, collapse every run
  // of non-alphanumerics into a single "-", and trim leading/trailing "-".
  const safe = branch
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')

  // `main` is production, and an empty/degenerate branch has no branch deploy —
  // both should just open the live site.
  if (!safe || safe === 'main') {
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

  const base = branchToOrigin(branch, origin)
  redirect(new URL(to, base).toString())
}
