import { config, collection, fields } from '@keystatic/core'

/**
 * Keystatic CMS configuration.
 *
 * STORAGE — auto-switches on whether GitHub mode has been configured, keyed on
 * the presence of NEXT_PUBLIC_KEYSTATIC_GITHUB_APP_SLUG:
 *   - NOT set (local dev today, and any build before you create the GitHub
 *     App): LOCAL mode. The admin reads/writes the filesystem directly
 *     (content/*.mdx); no GitHub App or network needed. NOTE: at ~860 posts the
 *     local collection list takes ~40s to load because Keystatic hashes every
 *     file for its git tree — a local-mode-only cost that GitHub mode removes.
 *   - SET (production, once configured): GITHUB mode. The deployed /keystatic
 *     signs in with GitHub and commits through a GitHub App. GitHub's API
 *     serves the file tree (no local hashing) and its CDN absorbs the per-file
 *     reads, so it stays fast at 860 entries — and you could re-enable list
 *     columns there if you want (see the `columns` note below).
 *
 * Why gate on the slug env var (not NODE_ENV)? A plain NODE_ENV switch turns on
 * GitHub mode for every production build, and Keystatic then fails the build if
 * the GitHub credentials aren't set yet. Gating on the app slug keeps builds
 * green until GitHub is actually configured, then flips automatically. The var
 * is NEXT_PUBLIC_* so the browser bundle and the server agree on the mode.
 *
 * TO FINISH GITHUB MODE (one-time):
 *   1. Deploy, then visit the deployed /keystatic — Keystatic walks you through
 *      creating a GitHub App for BumgeunSong/eddys-blog
 *      (https://keystatic.com/docs/github-mode).
 *   2. Set these env vars in the host (e.g. Vercel), then redeploy:
 *        KEYSTATIC_GITHUB_CLIENT_ID
 *        KEYSTATIC_GITHUB_CLIENT_SECRET
 *        KEYSTATIC_SECRET
 *        NEXT_PUBLIC_KEYSTATIC_GITHUB_APP_SLUG   (the app's slug — also the flag
 *                                                 that switches this config)
 *   The API route handler (app/api/keystatic/[...params]/route.ts) already
 *   forwards the secrets, so no other code change is needed.
 *
 * To pin one mode regardless, replace `storage` with a single literal, e.g.
 * `storage: { kind: 'local' }`.
 */
const useGitHub = Boolean(process.env.NEXT_PUBLIC_KEYSTATIC_GITHUB_APP_SLUG)

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
