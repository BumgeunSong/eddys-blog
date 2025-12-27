"""
Base classes and utilities shared across all scrapers.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional


@dataclass
class ArticleMetadata:
    """Metadata extracted from an article."""
    title: str
    published_date: Optional[str] = None
    tags: List[str] = None
    meta_description: Optional[str] = None
    meta_image: str = ""
    lang: str = "ko"

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

    def to_frontmatter(self) -> str:
        """Convert metadata to YAML frontmatter format."""
        lines = ["---"]
        lines.append(f"title: {self.title}")

        if self.published_date:
            lines.append(f"published_date: {self.published_date}")

        if self.tags:
            tags_str = ", ".join(self.tags)
            lines.append(f"tags: {tags_str}")

        if self.meta_description:
            lines.append(f"meta_description: {self.meta_description}")

        if self.meta_image:
            lines.append(f"meta_image: {self.meta_image}")

        lines.append(f"lang: {self.lang}")
        lines.append("---")

        return "\n".join(lines)


# ============================================================
# Shared Utilities
# ============================================================

def sanitize_slug(text: str) -> str:
    """
    Convert text to a filesystem-safe slug.

    Removes any non-alphanumeric characters except hyphens and underscores.

    Args:
        text: Raw text to convert

    Returns:
        Filesystem-safe slug string
    """
    safe_slug = re.sub(r"[^a-zA-Z0-9_-]", "-", text)
    # Remove consecutive hyphens
    safe_slug = re.sub(r"-+", "-", safe_slug)
    # Remove leading/trailing hyphens
    safe_slug = safe_slug.strip("-")
    return safe_slug or "article"


def to_kebab_case(name: str) -> str:
    """
    Convert camelCase or PascalCase to kebab-case.

    Examples:
        codeReviewChallenge -> code-review-challenge
        MyComponent -> my-component

    Args:
        name: camelCase or PascalCase string

    Returns:
        kebab-case string
    """
    # Insert hyphen before uppercase letters and convert to lowercase
    result = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    # Handle consecutive uppercase letters (e.g., HTTPServer -> http-server)
    result = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', result)
    return result.lower()


def normalize_whitespace(content: str) -> str:
    """
    Remove trailing spaces and excessive blank lines.

    Args:
        content: Raw content string

    Returns:
        Cleaned content string
    """
    # Remove trailing spaces at end of lines
    content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

    # Reduce multiple blank lines to single blank line
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

    return content


def remove_html_wrappers(content: str) -> str:
    """
    Remove div and span wrappers that pandoc preserves.

    Args:
        content: Markdown content with HTML wrappers

    Returns:
        Cleaned markdown content
    """
    # Remove div tags
    content = re.sub(
        r'<div[^>]*>\s*(<div[^>]*>\s*)*(<img[^>]*>\s*)*',
        '',
        content
    )
    content = re.sub(r'</div>\s*', '', content)

    # Remove empty span tags
    content = re.sub(r'<span[^>]*>.*?</span>', '', content)

    return content


def read_urls_from_file(file_path: str) -> Iterator[str]:
    """
    Read URLs from a text file.

    Format:
    - One URL per line
    - Lines starting with # are comments
    - Empty lines are ignored

    Args:
        file_path: Path to text file containing URLs

    Yields:
        URLs from the file
    """
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                yield line


def get_output_dir(platform: str) -> Path:
    """
    Get the output directory for a platform.

    Args:
        platform: Platform name (e.g., 'brunch', 'velog')

    Returns:
        Path to output directory
    """
    script_dir = Path(__file__).parent.parent
    return script_dir / f"{platform}_md"
