"""
Base class for web scrapers that fetch articles via HTTP.

Used by: Brunch, Velog, and other web-based platforms.
"""

import os
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from .base import (
    ArticleMetadata,
    get_output_dir,
    normalize_whitespace,
    read_urls_from_file,
    remove_html_wrappers,
)


class WebScraper(ABC):
    """
    Abstract base class for web-based article scrapers.

    Subclasses must implement:
    - platform: Platform name (e.g., 'brunch')
    - create_slug(url): Convert URL to filesystem slug
    - extract_content(html): Extract article content from HTML
    """

    platform: str = ""

    # HTTP headers for requests
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )

    def __init__(self):
        self.output_dir = get_output_dir(self.platform)

    # ============================================================
    # Abstract methods (must be implemented by subclasses)
    # ============================================================

    @abstractmethod
    def create_slug(self, url: str) -> str:
        """
        Convert article URL to a filesystem-safe slug.

        Args:
            url: Article URL

        Returns:
            Filesystem-safe slug
        """
        pass

    @abstractmethod
    def extract_content(self, html: str) -> Tuple[str, str, str, ArticleMetadata]:
        """
        Extract article content from raw HTML.

        Args:
            html: Raw HTML content

        Returns:
            Tuple of (title, author, article_html, metadata)
        """
        pass

    # ============================================================
    # Shared implementation
    # ============================================================

    def get_output_paths(self, url: str) -> Tuple[Path, Path, Path, Path]:
        """
        Generate all necessary file paths for a given article URL.

        Args:
            url: Article URL

        Returns:
            Tuple of (article_dir, html_path, markdown_path, media_dir)
        """
        slug = self.create_slug(url)
        article_dir = self.output_dir / slug
        html_path = article_dir / "article.html"
        markdown_path = article_dir / "article.md"
        media_dir = article_dir / "assets"

        return article_dir, html_path, markdown_path, media_dir

    def fetch_html(self, url: str) -> str:
        """
        Download raw HTML content from article URL.

        Args:
            url: Article URL

        Returns:
            Raw HTML content as string

        Raises:
            requests.HTTPError: If the request fails
        """
        headers = {
            "User-Agent": self.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.text

    def build_html_document(self, title: str, author: str, article_html: str) -> str:
        """
        Wrap article content in a complete HTML document for pandoc.

        Args:
            title: Article title
            author: Author name (optional)
            article_html: Main article content HTML

        Returns:
            Complete HTML document string
        """
        author_line = f"<p><em>by {author}</em></p>" if author else ""

        return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
</head>
<body>
  <h1>{title}</h1>
  {author_line}
  {article_html}
</body>
</html>
"""

    def convert_to_markdown(self, html_path: Path, markdown_path: Path, media_dir: Path) -> None:
        """
        Convert HTML to Markdown using pandoc.

        Args:
            html_path: Path to input HTML file
            markdown_path: Path to output Markdown file
            media_dir: Directory to extract images to
        """
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        media_dir.mkdir(parents=True, exist_ok=True)

        pandoc_command = [
            "pandoc",
            str(html_path),
            "-f", "html",
            "-t", "gfm",  # GitHub-flavored Markdown
            "--extract-media", str(media_dir),
            "-o", str(markdown_path),
            "--wrap=none",  # Prevent line wrapping
        ]

        print("Running:", " ".join(pandoc_command))
        subprocess.run(pandoc_command, check=True)

    def clean_markdown(self, markdown_path: Path) -> None:
        """
        Post-process markdown file to clean up formatting.

        Args:
            markdown_path: Path to markdown file to clean
        """
        content = markdown_path.read_text(encoding="utf-8")
        content = remove_html_wrappers(content)
        content = normalize_whitespace(content)
        markdown_path.write_text(content, encoding="utf-8")

    def add_frontmatter(self, markdown_path: Path, metadata: ArticleMetadata) -> None:
        """
        Add YAML frontmatter to the beginning of a markdown file.

        Args:
            markdown_path: Path to markdown file
            metadata: Metadata to add as frontmatter
        """
        content = markdown_path.read_text(encoding="utf-8")
        frontmatter = metadata.to_frontmatter()
        content_with_metadata = f"{frontmatter}\n\n{content}"
        markdown_path.write_text(content_with_metadata, encoding="utf-8")

    def process_url(self, url: str) -> None:
        """
        Process a single article URL: fetch, convert, and save.

        Args:
            url: Article URL to process
        """
        url = url.strip()
        if not url:
            return

        print(f"\n=== Processing: {url} ===")

        article_dir, html_path, markdown_path, media_dir = self.get_output_paths(url)
        article_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Fetch and extract content
            raw_html = self.fetch_html(url)
            title, author, article_html, metadata = self.extract_content(raw_html)

            # Build and save complete HTML
            complete_html = self.build_html_document(title, author, article_html)
            html_path.write_text(complete_html, encoding="utf-8")

            # Convert to Markdown
            self.convert_to_markdown(html_path, markdown_path, media_dir)
            self.clean_markdown(markdown_path)

            # Add metadata frontmatter
            self.add_frontmatter(markdown_path, metadata)

            print(f"Done: {markdown_path}")

        except Exception as e:
            print(f"Error processing {url}: {e}")

    def run(self, urls: List[str]) -> None:
        """
        Process multiple URLs or a file containing URLs.

        Args:
            urls: List of URLs or path to a file containing URLs
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if len(urls) == 1 and os.path.isfile(urls[0]):
            # Single argument is a file - read URLs from it
            for url in read_urls_from_file(urls[0]):
                self.process_url(url)
        else:
            # Arguments are URLs themselves
            for url in urls:
                self.process_url(url)
