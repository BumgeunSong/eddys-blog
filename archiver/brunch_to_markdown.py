#!/usr/bin/env python3
"""
Brunch Article to Markdown Converter

Downloads Brunch articles and converts them to clean Markdown format
with extracted images using pandoc.
"""
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# -------- Configuration --------
OUTPUT_BASE_DIR = "brunch_md"
PANDOC_BIN = "pandoc"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)
# -------------------------------


@dataclass
class ArticleMetadata:
    """Metadata extracted from a Brunch article."""
    title: str
    published_date: Optional[str] = None
    tags: List[str] = None
    meta_description: Optional[str] = None
    meta_image: str = "https://example.com/default-image.jpg"
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

        lines.append(f"meta_image: {self.meta_image}")
        lines.append(f"lang: {self.lang}")
        lines.append("---")

        return "\n".join(lines)


# ============================================================
# URL and Path Utilities
# ============================================================

def create_slug_from_url(url: str) -> str:
    """
    Convert a Brunch URL to a filesystem-friendly slug.

    Examples:
        https://brunch.co.kr/@bumgeunsong/160 -> bumgeunsong-160
        https://brunch.co.kr/@author/123 -> author-123

    Args:
        url: Full Brunch article URL

    Returns:
        Filesystem-safe slug string
    """
    parsed_url = urlparse(url)
    path_parts = [part for part in parsed_url.path.split("/") if part]

    if len(path_parts) >= 2 and path_parts[0].startswith("@"):
        author_name = path_parts[0][1:]  # Remove @ symbol
        article_id = path_parts[1]
        slug = f"{author_name}-{article_id}"
    else:
        slug = "-".join(path_parts) or "article"

    # Remove any non-alphanumeric characters except hyphens and underscores
    safe_slug = re.sub(r"[^a-zA-Z0-9_-]", "-", slug)
    return safe_slug or "article"


def create_output_paths(url: str) -> Tuple[str, str, str, str]:
    """
    Generate all necessary file paths for a given article URL.

    Args:
        url: Brunch article URL

    Returns:
        Tuple of (article_dir, html_path, markdown_path, media_dir)
    """
    slug = create_slug_from_url(url)
    article_dir = os.path.join(OUTPUT_BASE_DIR, slug)
    html_path = os.path.join(article_dir, "article.html")
    markdown_path = os.path.join(article_dir, "article.md")
    media_dir = os.path.join(article_dir, "assets")

    return article_dir, html_path, markdown_path, media_dir


# ============================================================
# HTML Fetching and Parsing
# ============================================================

def fetch_article_html(url: str) -> str:
    """
    Download raw HTML content from a Brunch article URL.

    Args:
        url: Brunch article URL

    Returns:
        Raw HTML content as string

    Raises:
        requests.HTTPError: If the request fails
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://brunch.co.kr/",
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    """Extract article title from parsed HTML."""
    title_element = soup.select_one("h1.cover_title")
    return title_element.get_text(strip=True) if title_element else "Untitled"


def extract_author(soup: BeautifulSoup) -> str:
    """Extract author name from parsed HTML."""
    author_element = soup.select_one("span.author_name")
    return author_element.get_text(strip=True) if author_element else ""


def extract_description(soup: BeautifulSoup) -> Optional[str]:
    """Extract article description/subtitle from parsed HTML."""
    desc_element = soup.select_one("p.cover_sub_title")
    return desc_element.get_text(strip=True) if desc_element else None


def extract_published_date(soup: BeautifulSoup) -> Optional[str]:
    """
    Extract and format published date from parsed HTML.

    Converts format like 'Oct 7. 2023' to '2023-10-07 00:00'
    """
    date_element = soup.select_one("span.f_l.date")
    if not date_element:
        return None

    date_text = date_element.get_text(strip=True)
    try:
        # Parse date like "Oct 7. 2023"
        parsed_date = datetime.strptime(date_text, "%b %d. %Y")
        return parsed_date.strftime("%Y-%m-%d 00:00")
    except ValueError:
        # If parsing fails, return the original text
        return date_text


def extract_tags(soup: BeautifulSoup) -> List[str]:
    """
    Extract keyword tags from parsed HTML.

    Looks for keywords in ul.list_keyword > li > a elements.
    """
    tags = []
    keyword_list = soup.select("ul.list_keyword li a.link_keyword")

    for keyword_link in keyword_list:
        tag = keyword_link.get_text(strip=True)
        if tag:
            tags.append(tag)

    return tags


def extract_cover_image(soup: BeautifulSoup) -> Optional[str]:
    """
    Extract cover image URL from div.cover_image style attribute.

    Parses the background-image CSS property to get the image URL.
    """
    cover_div = soup.select_one("div.cover_image")
    if not cover_div:
        return None

    style = cover_div.get("style", "")
    # Extract URL from background-image: url(...)
    match = re.search(r'url\(([^)]+)\)', style)
    if match:
        url = match.group(1).strip()
        # Add https: if URL starts with //
        if url.startswith("//"):
            url = "https:" + url
        return url
    return None


def extract_metadata(soup: BeautifulSoup) -> ArticleMetadata:
    """
    Extract all metadata from article HTML.

    Args:
        soup: BeautifulSoup parsed HTML

    Returns:
        ArticleMetadata object with all extracted fields
    """
    return ArticleMetadata(
        title=extract_title(soup),
        published_date=extract_published_date(soup),
        tags=extract_tags(soup),
        meta_description=extract_description(soup),
        meta_image=extract_cover_image(soup) or "https://example.com/default-image.jpg",
    )


def find_article_container(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Find the main article content container in the HTML.

    Tries multiple selectors in order of preference:
    1. div.item_view article
    2. div.wrap_body
    3. body tag (fallback)
    """
    container = soup.select_one("div.item_view article")
    if container is None:
        container = soup.select_one("div.wrap_body")
    if container is None:
        container = soup.body or soup
    return container


def fix_lazy_loaded_images(container: BeautifulSoup) -> None:
    """
    Fix lazy-loaded images by moving data-src to src attribute.

    Modifies the container in place.
    """
    for img in container.find_all("img"):
        if not img.get("src"):
            data_src = img.get("data-src") or img.get("data-lazy-src")
            if data_src:
                img["src"] = data_src


def remove_unwanted_tags(container: BeautifulSoup) -> None:
    """
    Remove script and style tags from container.

    Modifies the container in place.
    """
    for tag in container.find_all(["script", "style"]):
        tag.decompose()


def clean_vue_framework_markers(html: str) -> str:
    """
    Remove Vue.js framework comment markers and bracket sequences.

    Brunch uses Vue.js which adds markers like:
    - <!--[--> <!--]-->
    - [[[[![![[ ]]]]]]]]]

    Args:
        html: HTML string with Vue markers

    Returns:
        Cleaned HTML string
    """
    # Remove HTML comment markers
    html = re.sub(r'<!--\[-->', '', html)
    html = re.sub(r'<!--\]-->', '', html)
    html = re.sub(r'<!--\[!-->', '', html)
    html = re.sub(r'<!--\]!-->', '', html)
    html = re.sub(r'<!-- -->', '', html)

    # Remove bracket sequences (3+ consecutive brackets/exclamation marks)
    html = re.sub(r'[\[\]!]{3,}', '', html)

    return html


def extract_article_content(raw_html: str) -> Tuple[str, str, str, ArticleMetadata]:
    """
    Extract title, author, metadata, and clean article content from raw HTML.

    Args:
        raw_html: Full HTML page content

    Returns:
        Tuple of (title, author, article_html, metadata)
    """
    soup = BeautifulSoup(raw_html, "html.parser")

    title = extract_title(soup)
    author = extract_author(soup)
    metadata = extract_metadata(soup)
    container = find_article_container(soup)

    fix_lazy_loaded_images(container)
    remove_unwanted_tags(container)

    article_html = "".join(str(child) for child in container.children)
    article_html = clean_vue_framework_markers(article_html)

    return title, author, article_html, metadata


def build_complete_html_document(title: str, author: str, article_html: str) -> str:
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


# ============================================================
# Markdown Conversion and Cleanup
# ============================================================

def convert_html_to_markdown(html_path: str, markdown_path: str, media_dir: str) -> None:
    """
    Convert HTML to Markdown using pandoc.

    Args:
        html_path: Path to input HTML file
        markdown_path: Path to output Markdown file
        media_dir: Directory to extract images to
    """
    os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
    os.makedirs(media_dir, exist_ok=True)

    pandoc_command = [
        PANDOC_BIN,
        html_path,
        "-f", "html",
        "-t", "gfm",  # GitHub-flavored Markdown
        "--extract-media", media_dir,
        "-o", markdown_path,
        "--wrap=none",  # Prevent line wrapping
    ]

    print("Running:", " ".join(pandoc_command))
    subprocess.run(pandoc_command, check=True)


def remove_html_wrappers(content: str) -> str:
    """Remove div and span wrappers that pandoc preserves."""
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


def normalize_whitespace(content: str) -> str:
    """Remove trailing spaces and excessive blank lines."""
    # Remove trailing spaces at end of lines
    content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

    # Reduce multiple blank lines to single blank line
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

    return content


def add_frontmatter_to_markdown(markdown_path: str, metadata: ArticleMetadata) -> None:
    """
    Add YAML frontmatter to the beginning of a markdown file.

    Args:
        markdown_path: Path to markdown file
        metadata: Metadata to add as frontmatter
    """
    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Prepend frontmatter
    frontmatter = metadata.to_frontmatter()
    content_with_metadata = f"{frontmatter}\n\n{content}"

    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(content_with_metadata)


def clean_markdown_file(markdown_path: str) -> None:
    """
    Post-process markdown file to clean up formatting.

    Steps:
    1. Remove HTML div/span wrappers
    2. Remove trailing whitespace
    3. Normalize blank lines

    Args:
        markdown_path: Path to markdown file to clean
    """
    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = remove_html_wrappers(content)
    content = normalize_whitespace(content)

    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(content)


# ============================================================
# Main Processing Pipeline
# ============================================================

def save_html_file(html_content: str, file_path: str) -> None:
    """Save HTML content to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def process_single_article(url: str) -> None:
    """
    Process a single Brunch article URL: fetch, convert, and save.

    This is the main pipeline that orchestrates all steps:
    1. Fetch HTML from URL
    2. Extract content (title, author, body, metadata)
    3. Build complete HTML document
    4. Save HTML file
    5. Convert to Markdown with pandoc
    6. Clean up Markdown formatting
    7. Add frontmatter with metadata

    Args:
        url: Brunch article URL to process
    """
    url = url.strip()
    if not url:
        return

    print(f"\n=== Processing: {url} ===")

    article_dir, html_path, markdown_path, media_dir = create_output_paths(url)
    os.makedirs(article_dir, exist_ok=True)

    try:
        # Fetch and extract content
        raw_html = fetch_article_html(url)
        title, author, article_html, metadata = extract_article_content(raw_html)

        # Build and save complete HTML
        complete_html = build_complete_html_document(title, author, article_html)
        save_html_file(complete_html, html_path)

        # Convert to Markdown
        convert_html_to_markdown(html_path, markdown_path, media_dir)
        clean_markdown_file(markdown_path)

        # Add metadata frontmatter
        add_frontmatter_to_markdown(markdown_path, metadata)

        print(f"✓ Done: {markdown_path}")

    except Exception as e:
        print(f"✗ Error processing {url}: {e}")


def read_urls_from_file(file_path: str):
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


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert Brunch articles to Markdown with images using pandoc."
    )
    parser.add_argument(
        "urls",
        nargs="+",
        help=(
            "Either a list of Brunch URLs, or a path to a text file "
            "containing one URL per line."
        ),
    )
    args = parser.parse_args()

    # Process URLs
    if len(args.urls) == 1 and os.path.isfile(args.urls[0]):
        # Single argument is a file - read URLs from it
        for url in read_urls_from_file(args.urls[0]):
            process_single_article(url)
    else:
        # Arguments are URLs themselves
        for url in args.urls:
            process_single_article(url)


if __name__ == "__main__":
    main()
