# Writing Archiver

Extract articles from various platforms and migrate them to a unified format.

## Quick Start

```bash
cd archiver

# List available platforms
python scrape.py --list

# Scrape from web platforms
python scrape.py brunch https://brunch.co.kr/@author/123
python scrape.py velog https://velog.io/@author/post

# Scrape from local platforms
python scrape.py learning_man

# Scrape from a data-export archive
python scrape.py linkedin ~/Downloads/Complete_LinkedInDataExport_08-23-2026

# Migrate all to Nextra format
python migrate_articles.py

# Migrate a single platform (leaves the other platforms' files untouched)
python migrate_articles.py --source linkedin
```

## LinkedIn

LinkedIn has no usable API for your own writing, so the input is the unzipped
"Settings > Data privacy > Get a copy of your data > Download larger archive"
folder. Two kinds of writing come out of it:

| In the export | Becomes |
|---|---|
| `Shares_<memberid>.csv` | `content/linkedin-YYYYMMDD-HHMMSS.mdx` |
| `Articles/Articles/*.html` | `content/linkedin-article-<id>.mdx` |

Things the export gets wrong, which the scraper works around:

- **`ShareCommentary` quoting is broken.** The exporter closes and reopens the
  CSV quote around every newline, so a paragraph break arrives as `"\n""\n"`.
  Quotes the author typed are *not* escaped, so any global quote-stripping
  corrupts real text. See `unescape_share_commentary()`.
- **Article cover `<img src>` is a truncated stub** that 404s. The real cover
  comes from the live Pulse page's `og:image` (the page is public, no login).
- **Article image URLs expire** (`e=<unix ts>` in the query), so inline images
  and covers are downloaded into `assets/` instead of hotlinked.
- **Unpublished drafts ship alongside published articles** as `Copy of ...`
  with `Published on ---`. They're skipped.

Feed posts have no title, so one is derived from the opening sentence. Posts
shorter than `MIN_POST_LENGTH` are one-line reactions to someone else's post
rather than writing, and are skipped. Pure reposts never reach the scraper —
LinkedIn files them separately in `InstantReposts_*.csv` with no text.

## Directory Structure

```
archiver/
├── scrapers/                 # Modular scraper package
│   ├── base.py              # ArticleMetadata, shared utilities
│   ├── web_scraper.py       # Base class for HTTP scrapers
│   ├── local_scraper.py     # Base class for local file scrapers
│   ├── brunch.py            # Brunch extractor
│   ├── velog.py             # Velog extractor
│   ├── learning_man.py      # Learning Man extractor
│   └── linkedin.py          # LinkedIn data-export extractor
├── scrape.py                # Unified CLI
├── migrate_articles.py      # Migration to Nextra format
├── brunch_md/               # Raw Brunch articles
├── velog_md/                # Raw Velog articles
├── learning_man_md/         # Raw Learning Man articles
└── linkedin_md/             # Raw LinkedIn posts and articles
```

## Adding a New Platform

### Web Platform (HTTP-based)

1. Create `scrapers/newplatform.py`:

```python
from .base import ArticleMetadata, sanitize_slug
from .web_scraper import WebScraper

class NewPlatformScraper(WebScraper):
    platform = "newplatform"

    def create_slug(self, url: str) -> str:
        # Convert URL to filesystem slug
        return sanitize_slug(...)

    def extract_content(self, html: str):
        # Extract title, author, article_html, metadata
        return title, author, article_html, metadata
```

2. Add to `scrapers/__init__.py`:
```python
from .newplatform import NewPlatformScraper
```

3. Add to `scrape.py` SCRAPERS dict:
```python
SCRAPERS = {
    ...
    'newplatform': NewPlatformScraper,
}
```

4. Add to `migrate_articles.py` SOURCE_DIRS:
```python
SOURCE_DIRS = [
    ...
    ('newplatform_md', 'newplatform'),
]
```

### Local Platform (filesystem-based)

1. Create `scrapers/newblog.py`:

```python
from .base import ArticleMetadata
from .local_scraper import LocalScraper

class NewBlogScraper(LocalScraper):
    platform = "newblog"
    source_path = Path("/path/to/blog/content")

    def find_posts(self) -> List[Path]:
        # Return list of post paths
        ...

    def create_slug(self, post_path: Path) -> str:
        # Convert path to slug
        ...

    def extract_content(self, post_path: Path):
        # Return (metadata, body)
        ...
```

2. Follow steps 2-4 from web platform above.

## Output Format

Each scraped article produces:

```
{platform}_md/{slug}/
├── article.md      # Markdown with YAML frontmatter
└── assets/         # Extracted images
```

### Frontmatter Schema

```yaml
---
title: Article Title
published_date: 2024-01-15 10:30
tags: tag1, tag2
meta_description: Short description
meta_image: ./assets/cover.jpg
lang: ko
---
```

## Migration

`migrate_articles.py` transforms raw articles to Nextra format:

- Input: `{platform}_md/{slug}/article.md`
- Output: `content/{platform}-{slug}.mdx`
- Assets: `public/assets/posts/{platform}-{slug}/`
