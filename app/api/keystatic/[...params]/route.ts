import { makeRouteHandler } from '@keystatic/next/route-handler'
import config from '@/keystatic.config'

// Keystatic's API route: handles local-mode editor read/write operations under
// /api/keystatic/local/**. In LOCAL mode no GitHub credentials are required.
//
// When switching to GitHub mode (see keystatic.config.ts), pass the env vars:
//   makeRouteHandler({
//     config,
//     clientId: process.env.KEYSTATIC_GITHUB_CLIENT_ID,
//     clientSecret: process.env.KEYSTATIC_GITHUB_CLIENT_SECRET,
//     secret: process.env.KEYSTATIC_SECRET,
//   })
export const { POST, GET } = makeRouteHandler({
  config,
})
