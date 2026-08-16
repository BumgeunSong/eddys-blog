import { makeRouteHandler } from '@keystatic/next/route-handler'
import config from '@/keystatic.config'

// Keystatic's API route.
// - LOCAL mode (dev): handles editor read/write under /api/keystatic/local/**.
//   The GitHub env vars below are undefined and simply ignored.
// - GITHUB mode (prod): handles the OAuth login/callback and git operations.
//   Requires the KEYSTATIC_GITHUB_* / KEYSTATIC_SECRET env vars to be set
//   (see keystatic.config.ts). Passing them unconditionally is safe in both
//   modes — Keystatic only uses them when storage.kind === 'github'.
export const { POST, GET } = makeRouteHandler({
  config,
  clientId: process.env.KEYSTATIC_GITHUB_CLIENT_ID,
  clientSecret: process.env.KEYSTATIC_GITHUB_CLIENT_SECRET,
  secret: process.env.KEYSTATIC_SECRET,
})
