import { config, collection, fields } from '@keystatic/core'

/**
 * Keystatic CMS configuration.
 *
 * STORAGE — explicit flag NEXT_PUBLIC_KEYSTATIC_STORAGE:
 *   - unset / anything but 'github'  → LOCAL mode. The admin reads/writes the
 *     filesystem directly (content/*.mdx); no GitHub App or network needed.
 *     This is the default for `next dev` authoring and keeps `next build` green.
 *     NOTE: at ~860 posts the local collection list takes ~40s to load because
 *     Keystatic hashes every file for its git tree — a local-mode-only cost.
 *   - 'github'                       → GITHUB mode. /keystatic signs in with
 *     GitHub and commits through a GitHub App. GitHub's API serves the file
 *     tree (no local hashing) and its CDN absorbs the per-file reads, so it
 *     stays fast at 860 entries. REQUIRED on Vercel — the serverless filesystem
 *     is read-only, so local mode can't persist edits there.
 *
 * Why an explicit flag (not the app slug, and not NODE_ENV)?
 *   - The "Create GitHub App" walkthrough at /keystatic/setup ONLY renders in
 *     GitHub mode, and it is what PRODUCES the app slug + secrets. Gating GitHub
 *     mode on the slug was a deadlock: no slug → local mode → walkthrough never
 *     shows → slug never obtained. This flag lets you enter GitHub mode first.
 *   - A NODE_ENV switch would force GitHub mode on every prod build and fail the
 *     build when secrets aren't set yet. With this flag, builds without it stay
 *     in local mode and pass; you only set it once you're ready.
 *   The var is NEXT_PUBLIC_* so the browser bundle and server agree on the mode.
 *
 * ONE-TIME GITHUB SETUP (do the app creation LOCALLY — the prod build needs the
 * secrets, which don't exist until the app is created):
 *   1. Locally: `NEXT_PUBLIC_KEYSTATIC_STORAGE=github npm run dev`, open
 *      http://localhost:3000/keystatic/setup, and use "Create GitHub App"
 *      (Deployed App URL = https://www.eddysong.com). GitHub redirects back and
 *      Keystatic prints the 4 env vars — save them in .env.local:
 *        KEYSTATIC_GITHUB_CLIENT_ID
 *        KEYSTATIC_GITHUB_CLIENT_SECRET
 *        KEYSTATIC_SECRET
 *        NEXT_PUBLIC_KEYSTATIC_GITHUB_APP_SLUG
 *   2. In Vercel set those 4 vars PLUS  NEXT_PUBLIC_KEYSTATIC_STORAGE=github,
 *      then redeploy. The route handler (app/api/keystatic/[...params]/route.ts)
 *      already forwards the secrets.
 *   Docs: https://keystatic.com/docs/github-mode
 *
 * To pin one mode regardless, replace `storage` with a single literal, e.g.
 * `storage: { kind: 'local' }`.
 */
const useGitHub = process.env.NEXT_PUBLIC_KEYSTATIC_STORAGE === 'github'

export default config({
  storage: useGitHub
    ? { kind: 'github', repo: { owner: 'BumgeunSong', name: 'eddys-blog' } }
    : { kind: 'local' },

  ui: {
    brand: { name: '에디의 블로그 CMS' },
  },

  collections: {
    posts: collection({
      label: 'Posts',

      // Existing posts are flat `content/{slug}.mdx` files. A flat `*` glob keeps
      // Keystatic writing single files per entry (a `**` or `/{slug}` path would
      // instead create a folder-per-entry with an index file).
      path: 'content/*',

      // Single-file output: YAML frontmatter (data, defaults to yaml) + the body
      // taken from the `content` field. The content field is `fields.mdx` below,
      // which fixes the file extension to `.mdx` so entries stay identical in
      // shape to the existing posts.
      format: { contentField: 'content' },

      // The slug drives the filename: content/{slug}.mdx
      slugField: 'title',

      // NOTE: no `columns` here on purpose. Adding non-slug columns (e.g.
      // ['title', 'date']) makes Keystatic read EVERY entry's file to fill the
      // list view. With ~860 posts, LOCAL mode fires hundreds of concurrent
      // requests and the browser aborts them (net::ERR_INSUFFICIENT_RESOURCES).
      // The default list shows the slug only, which comes from the file tree in
      // a single request.
      //
      // In GITHUB mode (production) GitHub's CDN handles that fan-out far
      // better, so you can experiment with re-enabling columns THERE — e.g.:
      //   columns: useGitHub ? ['title', 'date'] : undefined,
      // (Left off entirely for now to keep behaviour identical in both modes.)

      schema: {
        // `fields.slug` stores the human name under `title:` in frontmatter and
        // uses the slug portion as the filename (no separate `slug:` key is
        // written — matching the existing files).
        title: fields.slug({
          name: { label: 'Title' },
          slug: {
            label: 'Slug (filename)',
            description: 'Drives the filename: content/{slug}.mdx',
          },
        }),

        date: fields.date({
          label: 'Date',
          defaultValue: { kind: 'today' },
          validation: { isRequired: true },
        }),

        source: fields.text({
          label: 'Source',
          description: 'Origin platform. Use "blog" for hand-written posts.',
          defaultValue: 'blog',
        }),

        visibility: fields.select({
          label: 'Visibility',
          description: 'Private posts are filtered out of the public listing.',
          options: [
            { label: 'Public', value: 'public' },
            { label: 'Private', value: 'private' },
          ],
          defaultValue: 'public',
        }),

        tags: fields.array(fields.text({ label: 'Tag' }), {
          label: 'Tags',
          itemLabel: (props) => props.value || 'Tag',
        }),

        description: fields.text({
          label: 'Description',
          multiline: true,
        }),

        // Optional cover image. Stored as a plain path string (e.g.
        // /assets/posts/foo.png) to match the existing frontmatter convention,
        // rather than an uploaded asset.
        image: fields.text({
          label: 'Image',
          description: 'Optional cover image path, e.g. /assets/posts/....',
        }),

        // The MDX body. Serialized below the frontmatter as the `.mdx` body.
        content: fields.mdx({ label: 'Body' }),
      },
    }),
  },
})
