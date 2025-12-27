# 에디의 블로그

A personal blog built with [Nextra](https://nextra.site/) that archives writings from Korean publishing platforms.

## Development

```bash
npm install
npm run dev
```

## Archiving Articles

Archiving scripts are in the `archiver/` directory.

### Single Article

```bash
# Brunch
python3 archiver/brunch_to_markdown.py "https://brunch.co.kr/@bumgeunsong/160"

# Velog
python3 archiver/velog_to_markdown.py "https://velog.io/@eddy_song/article-slug"
```

### Migration to Blog

After archiving, run the migration script to convert articles to Nextra format:

```bash
python3 archiver/migrate_articles.py
```

This converts articles from `archiver/brunch_md/` and `archiver/velog_md/` to `content/` directory.

## Deployment

1. Push to GitHub
2. Connect to Vercel
3. Auto-deploys on push

## Project Structure

```
writing-archiver/
├── archiver/                  # Archiving scripts
│   ├── brunch_to_markdown.py
│   ├── velog_to_markdown.py
│   ├── migrate_articles.py
│   ├── brunch_md/             # Archived Brunch articles
│   └── velog_md/              # Archived Velog articles
├── app/                       # Nextra blog
│   ├── layout.jsx
│   ├── page.mdx               # Home page
│   └── posts/
│       ├── page.jsx           # Posts listing
│       └── [...slug]/         # Individual posts
├── content/                   # MDX posts (after migration)
├── public/
│   └── assets/posts/          # Post images
├── package.json
└── next.config.mjs
```

## Supported Platforms

| Platform | Status |
|----------|--------|
| [Brunch](https://brunch.co.kr) | Supported |
| [Velog](https://velog.io) | Supported |

## Requirements

- Node.js 18+
- Python 3.x
- [Pandoc](https://pandoc.org/installing.html)
