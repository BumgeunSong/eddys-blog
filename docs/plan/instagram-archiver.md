# Instagram Posts Archiver Plan

## Overview
Archive Instagram posts to MDX format using the **Instagram Data Export** approach (JSON download from Instagram Settings).

## Step 1: Export Your Instagram Data (Manual)

1. Go to Instagram → Settings → Your Activity → Download Your Information
2. Select "Some of Your Information"
3. Choose:
   - **Your Instagram activity → Content** (posts with captions)
   - **Media** (actual images/videos)
4. Configure:
   - **Format**: JSON
   - **Media Quality**: High
   - **Date Range**: All Time
5. Wait for email notification (up to 48 hours)
6. Download the ZIP file within 4 days
7. Extract to `archiver/instagram_export/`

## Step 2: Create Instagram Scraper

Create `archiver/scrapers/instagram.py` extending `LocalScraper`:

```python
class InstagramScraper(LocalScraper):
    """Scraper for Instagram data export (JSON files)."""

    platform = "instagram"
    source_path = SCRIPT_DIR.parent / "instagram_export"

    def find_posts(self) -> List[Path]:
        # Read content/posts_1.json
        # Return list of post entries

    def create_slug(self, post_path: Path) -> str:
        # Use timestamp: {YYYYMMDD-HHMMSS}

    def extract_content(self, post_path: Path) -> Tuple[ArticleMetadata, str]:
        # Extract: caption, timestamp, media paths
        # Parse hashtags from caption as tags
```

### Instagram Export Structure:
```
instagram_export/
├── content/
│   └── posts_1.json          # Post metadata
└── media/
    └── posts/
        └── 202312_123456.jpg  # Media files
```

### posts_1.json format:
```json
[
  {
    "media": [
      {
        "uri": "media/posts/202312_123456.jpg",
        "creation_timestamp": 1703123456,
        "title": "Caption text here"
      }
    ],
    "title": "Caption or empty"
  }
]
```

### Metadata Mapping:
| Instagram | ArticleMetadata |
|-----------|-----------------|
| `title` or `media[0].title` | `title` (first 50 chars) |
| `creation_timestamp` | `published_date` |
| Hashtags in caption | `tags` |
| Caption text | `meta_description` |
| First image | `meta_image` |

## Step 3: Register Scraper

Update `archiver/scrapers/__init__.py`:
```python
from .instagram import InstagramScraper

__all__ = [
    'BrunchScraper',
    'VelogScraper',
    'LearningManScraper',
    'InstagramScraper',  # Add
]
```

Update `archiver/scrape.py`:
```python
from scrapers import BrunchScraper, VelogScraper, LearningManScraper, InstagramScraper

SCRAPERS = {
    'brunch': BrunchScraper,
    'velog': VelogScraper,
    'learning_man': LearningManScraper,
    'instagram': InstagramScraper,  # Add
}
```

## Step 4: Update Migration Script

Update `archiver/migrate_articles.py`:
```python
SOURCE_DIRS = [
    ('brunch_md', 'brunch'),
    ('velog_md', 'velog'),
    ('learning_man_md', 'learning_man'),
    ('instagram_md', 'instagram'),  # Add
]
```

## Files to Create/Modify

| File | Action |
|------|--------|
| `archiver/scrapers/instagram.py` | Create |
| `archiver/scrapers/__init__.py` | Add InstagramScraper |
| `archiver/scrape.py` | Add instagram to SCRAPERS |
| `archiver/migrate_articles.py` | Add instagram_md source |
| `readme.md` | Add Instagram to supported platforms |

## Usage (After Implementation)

```bash
# 1. Place exported ZIP contents in archiver/instagram_export/
# 2. Run scraper
python3 archiver/scrape.py instagram

# 3. Migrate to Nextra format
python3 archiver/migrate_articles.py
```

## Special Handling

- **Hashtag extraction**: Parse `#tag` from caption → add to tags
- **Multi-image posts**: Include all images in markdown
- **Unicode/Emoji**: Handle UTF-8 encoding properly
- **Empty captions**: Use date as title fallback
- **Media paths**: Copy from `media/posts/` to `{slug}/assets/`
