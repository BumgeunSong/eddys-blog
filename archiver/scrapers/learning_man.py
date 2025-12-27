"""
Learning Man Gatsby blog scraper.

Extracts posts from a local Gatsby blog, filtered by author.
"""

import re
from pathlib import Path
from typing import List, Tuple

from .base import ArticleMetadata, to_kebab_case
from .local_scraper import LocalScraper


class LearningManScraper(LocalScraper):
    """Scraper for Learning Man Gatsby blog (local filesystem)."""

    platform = "learning_man"
    source_path = Path.home() / "coding" / "Learning_man" / "learningman_blog" / "content" / "blog"
    author = "eddy"

    def find_posts(self) -> List[Path]:
        """Find all posts by the configured author."""
        matching_posts = []

        if not self.source_path.exists():
            print(f"Blog path not found: {self.source_path}")
            return matching_posts

        for post_dir in self.source_path.iterdir():
            if not post_dir.is_dir():
                continue

            index_file = post_dir / "index.md"
            if not index_file.exists():
                continue

            content = index_file.read_text(encoding="utf-8")
            frontmatter, _ = self.parse_frontmatter(content)

            tags = frontmatter.get("tags", [])
            if isinstance(tags, list) and self.author in tags:
                matching_posts.append(post_dir)

        return matching_posts

    def create_slug(self, post_path: Path) -> str:
        """Convert post folder name to kebab-case slug."""
        return to_kebab_case(post_path.name)

    def extract_content(self, post_path: Path) -> Tuple[ArticleMetadata, str]:
        """Extract metadata and content from a Gatsby post."""
        index_file = post_path / "index.md"
        content = index_file.read_text(encoding="utf-8")
        frontmatter, body = self.parse_frontmatter(content)

        # Extract and clean title
        title = frontmatter.get("title", "Untitled")
        if title.startswith('"') and title.endswith('"'):
            title = title[1:-1]

        # Format date
        date_str = frontmatter.get("date", "")
        published_date = self._format_date(date_str)

        # Filter out author tag
        raw_tags = frontmatter.get("tags", [])
        if isinstance(raw_tags, list):
            tags = [t for t in raw_tags if t != self.author]
        else:
            tags = []

        # Get description
        description = frontmatter.get("description", "")

        # Determine meta_image path
        og_image = frontmatter.get("ogimage", "")
        meta_image = ""
        if og_image and og_image.startswith("./"):
            image_name = og_image[2:]  # Remove "./"
            meta_image = f"./assets/{image_name}"
        else:
            # Check for images in directory
            images = self.find_images(post_path)
            if images:
                meta_image = f"./assets/{images[0].name}"

        metadata = ArticleMetadata(
            title=title,
            published_date=published_date,
            tags=tags,
            meta_description=description,
            meta_image=meta_image,
        )

        return metadata, body

    def _format_date(self, iso_date: str) -> str:
        """
        Convert ISO 8601 date to YYYY-MM-DD HH:MM format.

        Args:
            iso_date: Date string like "2020-10-04T06:40:32.169Z"

        Returns:
            Formatted date like "2020-10-04 06:40"
        """
        if not iso_date:
            return ""

        match = re.match(r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})', iso_date)
        if match:
            return f"{match.group(1)} {match.group(2)}"

        if "T" in iso_date:
            return iso_date.split("T")[0] + " 00:00"

        return iso_date
