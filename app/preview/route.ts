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
// A single DNS label (the subdomain) can be at most 63 chars. Beyond that Vercel
// truncates the branch and appends a hash we can't reproduce, so the host 404s.
const MAX_SUBDOMAIN_LABEL = 63

function branchToOrigin(branch: string, origin: string): string {
  // `main` is production. Compare the RAW ref: branch names are case-sensitive,
  // so "MAIN" or "main_" are distinct branches and must reach their own deploy —
  // don't let sanitization collapse them onto production.
  if (branch === 'main') {
    return origin
  }

  // Mirror Vercel's branch → subdomain transform: lowercase, collapse every run
  // of non-alphanumerics into a single "-", and trim leading/trailing "-".
  const safe = branch
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')

  // Nothing usable to build a host from → fall back to production rather than
  // emit a broken URL.
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

  // Reject branches whose subdomain would exceed the DNS label limit: the
  // resulting Vercel host wouldn't exist, so fail loudly instead of redirecting
  // an editor to a dead link.
  if (base.hostname.split('.')[0].length > MAX_SUBDOMAIN_LABEL) {
    return new Response(
      'Branch name is too long for a Vercel preview subdomain — use a shorter branch name.',
      { status: 400 },
    )
  }

  // Guard against open redirects: `to` is request-controlled, and an absolute or
  // protocol-relative URL would otherwise override `base` and send the visitor
  // off-site. Only allow targets that resolve to a path on `base`'s own origin.
  const target = new URL(to, base)
  if (target.origin !== base.origin) {
    return new Response('Invalid "to" target — must be a path on the preview origin.', {
      status: 400,
    })
  }

  redirect(target.toString())
}
