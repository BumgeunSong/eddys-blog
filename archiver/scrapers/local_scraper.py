"""
Base class for local file scrapers that read from the filesystem.

Used by: Learning Man, and other local Gatsby/Hugo/Jekyll blogs.
"""

import re
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple

import yaml

from .base import ArticleMetadata, get_output_dir


class LocalScraper(ABC):
    """
    Abstract base class for local file-based article scrapers.

    Subclasses must implement:
    - platform: Platform name (e.g., 'learning_man')
    - source_path: Path to source blog content
    - find_posts(): Find all posts to process
    - create_slug(post_path): Convert post path to slug
    - extract_content(post_path): Extract content and metadata
    """

    platform: str = ""
    source_path: Path = None

    def __init__(self):
        self.output_dir = get_output_dir(self.platform)

    # ============================================================
    # Abstract methods (must be implemented by subclasses)
    # ============================================================

    @abstractmethod
    def find_posts(self) -> List[Path]:
        """
        Find all posts to process.

        Returns:
            List of paths to post directories or files
        """
        pass

    @abstractmethod
    def create_slug(self, post_path: Path) -> str:
        """
        Convert post path to a filesystem-safe slug.

        Args:
            post_path: Path to post directory or file

        Returns:
            Filesystem-safe slug
        """
        pass

    @abstractmethod
    def extract_content(self, post_path: Path) -> Tuple[ArticleMetadata, str]:
        """
        Extract metadata and content from a post.

        Args:
            post_path: Path to post directory or file

        Returns:
            Tuple of (metadata, markdown_body)
        """
        pass

    # ============================================================
    # Shared implementation
    # ============================================================

    def parse_frontmatter(self, content: str) -> Tuple[dict, str]:
        """
        Extract YAML frontmatter and body from markdown content.

        Args:
            content: Full markdown file content

        Returns:
            Tuple of (frontmatter dict, body text)
        """
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)

        if match:
            fm_text = match.group(1)
            body = match.group(2)
            try:
                frontmatter = yaml.safe_load(fm_text) or {}
            except yaml.YAMLError:
                frontmatter = {}
            return frontmatter, body

        return {}, content

    def find_images(self, post_path: Path) -> List[Path]:
        """
        Find all image files in a post directory.

        Args:
            post_path: Path to post directory

        Returns:
            List of image file paths
        """
        image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
        images = []

        if post_path.is_dir():
            for item in post_path.iterdir():
                if item.is_file() and item.suffix.lower() in image_extensions:
                    images.append(item)

        return images

    def update_image_paths(self, body: str, images: List[Path]) -> str:
        """
        Update image paths in markdown body to use ./assets/ paths.

        Args:
            body: Markdown body content
            images: List of image files in the post

        Returns:
            Updated body with corrected image paths
        """
        for image in images:
            # Common patterns for image references
            old_patterns = [
                f"./{image.name}",
                image.name,
                f"/{image.name}",
            ]
            new_path = f"./assets/{image.name}"

            for old_pattern in old_patterns:
                body = body.replace(f"]({old_pattern})", f"]({new_path})")

        return body

    def transform_post(self, post_path: Path) -> Optional[str]:
        """
        Transform a single post to archiver format.

        Args:
            post_path: Path to source post

        Returns:
            Output slug if successful, None otherwise
        """
        try:
            # Extract content
            metadata, body = self.extract_content(post_path)

            if not metadata.title:
                print(f"  Skipping {post_path.name}: no title found")
                return None

            # Create output directories
            slug = self.create_slug(post_path)
            output_dir = self.output_dir / slug
            assets_dir = output_dir / "assets"

            output_dir.mkdir(parents=True, exist_ok=True)
            assets_dir.mkdir(exist_ok=True)

            # Find and copy images
            images = self.find_images(post_path)
            for image in images:
                shutil.copy2(image, assets_dir / image.name)

            # Update image paths in body
            body = self.update_image_paths(body, images)

            # Write article.md
            output_content = metadata.to_frontmatter() + "\n\n" + body.strip() + "\n"
            output_file = output_dir / "article.md"
            output_file.write_text(output_content, encoding="utf-8")

            return slug

        except Exception as e:
            print(f"  Error processing {post_path.name}: {e}")
            return None

    def run(self, args: List[str] = None) -> None:
        """
        Process all posts from the source.

        Args:
            args: Optional arguments (ignored for local scrapers)
        """
        print(f"{self.platform.replace('_', ' ').title()} Extractor")
        print("=" * 40)
        print(f"Source: {self.source_path}")
        print(f"Output: {self.output_dir}")
        print()

        # Find posts
        posts = self.find_posts()
        print(f"Found {len(posts)} posts")
        print()

        if not posts:
            print("No posts found. Check the source path.")
            return

        # Process each post
        self.output_dir.mkdir(parents=True, exist_ok=True)
        successful = 0

        for post_path in sorted(posts):
            print(f"Processing: {post_path.name}")
            slug = self.transform_post(post_path)
            if slug:
                print(f"  -> {slug}/article.md")
                successful += 1

        print()
        print(f"Done! Processed {successful}/{len(posts)} posts.")
        print(f"Output: {self.output_dir}")
