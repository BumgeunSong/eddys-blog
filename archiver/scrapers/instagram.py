"""
Instagram post archiver.

Reads from Instagram data export (JSON) and converts to markdown format.
"""

import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from .base import ArticleMetadata, get_output_dir


@dataclass
class InstagramPost:
    """Represents an Instagram post."""
    uri: str
    creation_timestamp: int
    title: str  # Caption
    media_uris: List[str]  # All media files for this post


class InstagramScraper:
    """Scraper for Instagram data export (JSON files)."""

    platform = "instagram"

    def __init__(self, export_path: Optional[Path] = None):
        """
        Initialize scraper.

        Args:
            export_path: Path to Instagram export directory.
                        Auto-detects if not provided.
        """
        self.export_path = export_path or self._find_export_path()
        self.output_dir = get_output_dir(self.platform)

    def _find_export_path(self) -> Path:
        """Find the Instagram export directory."""
        base = Path(__file__).parent.parent / "instagram_export"
        if not base.exists():
            raise FileNotFoundError(f"Instagram export not found at {base}")

        # Find the actual export folder (instagram-username-date-id format)
        for item in base.iterdir():
            if item.is_dir() and item.name.startswith("instagram-"):
                return item

        raise FileNotFoundError("No Instagram export folder found")

    def _fix_encoding(self, text: str) -> str:
        """Fix Instagram's UTF-8-as-Latin-1 encoding issue."""
        if not text:
            return ""
        try:
            return text.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            return text

    def load_posts(self) -> List[InstagramPost]:
        """Load all posts from the export JSON."""
        posts_file = self.export_path / "your_instagram_activity" / "media" / "posts_1.json"
        if not posts_file.exists():
            raise FileNotFoundError(f"posts_1.json not found at {posts_file}")

        with open(posts_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        posts = []
        for item in data:
            media_list = item.get('media', [])
            if not media_list:
                continue

            # Get all media URIs for this post
            media_uris = [m.get('uri', '') for m in media_list]

            # Get caption from first media item or post title
            first_media = media_list[0]
            caption = first_media.get('title', '') or item.get('title', '')
            caption = self._fix_encoding(caption)

            post = InstagramPost(
                uri=first_media.get('uri', ''),
                creation_timestamp=first_media.get('creation_timestamp', 0),
                title=caption,
                media_uris=media_uris,
            )
            posts.append(post)

        return posts

    def create_slug(self, post: InstagramPost) -> str:
        """Create slug from timestamp."""
        dt = datetime.fromtimestamp(post.creation_timestamp)
        return dt.strftime("%Y%m%d-%H%M%S")

    def extract_hashtags(self, caption: str) -> List[str]:
        """Extract hashtags from caption."""
        if not caption:
            return []
        hashtags = re.findall(r'#(\w+)', caption)
        return hashtags[:10]  # Limit to 10 tags

    def get_title_from_caption(self, caption: str) -> str:
        """Extract title from caption (first 50 chars or first line)."""
        if not caption:
            return "Instagram Post"

        # Remove hashtags for title
        title = re.sub(r'#\w+\s*', '', caption)
        # Get first line
        title = title.split('\n')[0].strip()
        # Truncate
        if len(title) > 50:
            title = title[:47] + "..."
        return title or "Instagram Post"

    def create_metadata(self, post: InstagramPost) -> ArticleMetadata:
        """Create ArticleMetadata from post."""
        dt = datetime.fromtimestamp(post.creation_timestamp)

        return ArticleMetadata(
            title=self.get_title_from_caption(post.title),
            published_date=dt.strftime("%Y-%m-%d %H:%M"),
            tags=self.extract_hashtags(post.title),
            meta_description=post.title[:200] if post.title else "",
            lang="ko",
        )

    def create_markdown_content(self, post: InstagramPost, slug: str) -> str:
        """Create markdown content for the post."""
        lines = []

        # Add caption
        if post.title:
            # Clean up caption (remove excessive newlines)
            caption = re.sub(r'\n{3,}', '\n\n', post.title)
            lines.append(caption)
            lines.append("")

        # Add images
        for i, uri in enumerate(post.media_uris):
            filename = Path(uri).name
            # Image will be in ./assets/ folder
            lines.append(f"![image](./assets/{filename})")
            lines.append("")

        return "\n".join(lines)

    def save_post(self, post: InstagramPost) -> Path:
        """Save a single post to markdown file."""
        slug = self.create_slug(post)
        post_dir = self.output_dir / slug
        post_dir.mkdir(parents=True, exist_ok=True)

        # Create metadata and content
        metadata = self.create_metadata(post)
        content = self.create_markdown_content(post, slug)

        # Write markdown file
        full_content = metadata.to_frontmatter() + "\n\n" + content
        output_path = post_dir / "article.md"
        output_path.write_text(full_content, encoding="utf-8")

        # Copy media files
        assets_dir = post_dir / "assets"
        assets_dir.mkdir(exist_ok=True)

        for uri in post.media_uris:
            src = self.export_path / uri
            if src.exists():
                dst = assets_dir / src.name
                shutil.copy2(src, dst)

        return output_path

    def archive_all(self) -> int:
        """Archive all posts."""
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load posts
        posts = self.load_posts()
        print(f"Found {len(posts)} Instagram posts")

        # Save each post
        for i, post in enumerate(posts, 1):
            self.save_post(post)
            if i % 50 == 0:
                print(f"  Saved {i}/{len(posts)} posts...")

        print(f"Archived {len(posts)} posts to {self.output_dir}")
        return len(posts)


def main():
    """Main entry point."""
    scraper = InstagramScraper()
    scraper.archive_all()


if __name__ == "__main__":
    main()
