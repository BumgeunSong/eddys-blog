# Facebook Posts Archiver Plan

## Overview
Archive Facebook posts to MDX format using the **Facebook Data Export** approach (JSON download from Facebook Settings).

## Step 1: Export Your Facebook Data (Manual)

1. Go to Facebook → Settings & Privacy → Settings
2. Click "Your information" → "Download your information"
3. Configure export:
   - **Format**: JSON (important!)
   - **Media Quality**: High
   - **Date Range**: All Time (or custom)
   - **Information**: Select "Posts" (and optionally "Photos and videos")
4. Click "Create File" and wait for email notification
5. Download the ZIP file and extract to `archiver/facebook_export/`

## Step 2: Create Facebook Parser Script

Create `archiver/facebook_to_markdown.py` following existing patterns:

### Key Components:
```
archiver/
├── facebook_to_markdown.py  # New parser script
├── facebook_export/          # Place extracted JSON here
│   └── your_activity_across_facebook/
│       └── posts/
│           └── your_posts_1.json
└── facebook_md/              # Output directory
    └── {slug}/
        ├── article.md
        └── assets/
```

### Facebook JSON Structure (posts/your_posts_1.json):
```json
[
  {
    "timestamp": 1703123456,
    "data": [
      {"post": "Post text content here"}
    ],
    "attachments": [
      {
        "data": [
          {"media": {"uri": "photos_and_videos/...", "title": "..."}}
        ]
      }
    ],
    "title": "Author updated their status"
  }
]
```

### Metadata Extraction:
- **title**: First 50 chars of post text or "Facebook Post"
- **published_date**: Convert Unix timestamp to "YYYY-MM-DD HH:MM"
- **description**: First 150 chars of post text
- **meta_image**: First attached image path
- **tags**: Empty (Facebook posts don't have tags)

### Implementation Pattern (same as brunch/velog):
1. Read JSON from `facebook_export/` directory
2. Parse each post entry
3. Extract text content and media attachments
4. Copy images to `assets/` folder
5. Generate markdown with YAML frontmatter
6. Save to `facebook_md/{slug}/article.md`

## Step 3: Update Migration Script

Modify `archiver/migrate_articles.py`:
- Add `facebook_md/` as source directory
- Use `facebook-{index}` as slug format
- Handle Facebook-specific content (links, unicode emojis)

## Step 4: Update README

Add Facebook to supported platforms table.

## Files to Create/Modify

| File | Action |
|------|--------|
| `archiver/facebook_to_markdown.py` | Create |
| `archiver/migrate_articles.py` | Modify (add facebook source) |
| `readme.md` | Update supported platforms |

## Usage (After Implementation)

```bash
# 1. Place exported JSON in archiver/facebook_export/
# 2. Run parser
python3 archiver/facebook_to_markdown.py

# 3. Migrate to Nextra format
python3 archiver/migrate_articles.py
```

## Notes

- Facebook text encoding may need UTF-8 handling (emoji, Korean text)
- Some posts may be empty (shares without text) - skip these
- Image paths in JSON are relative to the export folder
- Consider filtering by post type (status updates only vs. all)
