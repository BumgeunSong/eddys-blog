import { config, collection, fields } from '@keystatic/core'

/**
 * Keystatic CMS configuration.
 *
 * STORAGE — currently LOCAL mode: the admin UI reads and writes the local
 * filesystem directly, so entries land in `content/*.mdx` exactly like the
 * existing hand-migrated posts.
 *
 * To switch to GitHub mode later (edit via the deployed site, commit through a
 * GitHub App), replace the `storage` block below with:
 *
 *   storage: {
 *     kind: 'github',
 *     repo: { owner: 'BumgeunSong', name: '<repo-name>' },
 *   },
 *
 * then create a GitHub App (https://keystatic.com/docs/github-mode) and set
 *   KEYSTATIC_GITHUB_CLIENT_ID
 *   KEYSTATIC_GITHUB_CLIENT_SECRET
 *   KEYSTATIC_SECRET
 * in the environment. The API route handler (app/api/keystatic/[...params]/route.ts)
 * already forwards those variables, so no other code change is needed.
 */
export default config({
  storage: { kind: 'local' },

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

      // Columns shown in the collection list view.
      columns: ['title', 'date'],

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
