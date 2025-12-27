"""
Brunch article scraper.

Extracts articles from brunch.co.kr.
"""

import re
from datetime import datetime
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .base import ArticleMetadata, sanitize_slug
from .web_scraper import WebScraper


class BrunchScraper(WebScraper):
    """Scraper for Brunch articles (brunch.co.kr)."""

    platform = "brunch"

    def create_slug(self, url: str) -> str:
        """
        Convert Brunch URL to slug.

        Examples:
            https://brunch.co.kr/@bumgeunsong/160 -> bumgeunsong-160
        """
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split("/") if part]

        if len(path_parts) >= 2 and path_parts[0].startswith("@"):
            author_name = path_parts[0][1:]  # Remove @ symbol
            article_id = path_parts[1]
            slug = f"{author_name}-{article_id}"
        else:
            slug = "-".join(path_parts) or "article"

        return sanitize_slug(slug)

    def extract_content(self, html: str) -> Tuple[str, str, str, ArticleMetadata]:
        """Extract article content from Brunch HTML."""
        soup = BeautifulSoup(html, "html.parser")

        title = self._extract_title(soup)
        author = self._extract_author(soup)
        metadata = self._extract_metadata(soup)
        article_html = self._extract_article_html(soup)

        return title, author, article_html, metadata

    # ============================================================
    # Brunch-specific extractors
    # ============================================================

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title."""
        title_element = soup.select_one("h1.cover_title")
        return title_element.get_text(strip=True) if title_element else "Untitled"

    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract author name."""
        author_element = soup.select_one("span.author_name")
        return author_element.get_text(strip=True) if author_element else ""

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article description/subtitle."""
        desc_element = soup.select_one("p.cover_sub_title")
        return desc_element.get_text(strip=True) if desc_element else None

    def _extract_published_date(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract and format published date.

        Converts format like 'Oct 7. 2023' to '2023-10-07 00:00'
        """
        date_element = soup.select_one("span.f_l.date")
        if not date_element:
            return None

        date_text = date_element.get_text(strip=True)
        try:
            parsed_date = datetime.strptime(date_text, "%b %d. %Y")
            return parsed_date.strftime("%Y-%m-%d 00:00")
        except ValueError:
            return date_text

    def _extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """Extract keyword tags."""
        tags = []
        keyword_list = soup.select("ul.list_keyword li a.link_keyword")

        for keyword_link in keyword_list:
            tag = keyword_link.get_text(strip=True)
            if tag:
                tags.append(tag)

        return tags

    def _extract_cover_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract cover image URL from div.cover_image style attribute."""
        cover_div = soup.select_one("div.cover_image")
        if not cover_div:
            return None

        style = cover_div.get("style", "")
        match = re.search(r'url\(([^)]+)\)', style)
        if match:
            url = match.group(1).strip()
            if url.startswith("//"):
                url = "https:" + url
            return url
        return None

    def _extract_metadata(self, soup: BeautifulSoup) -> ArticleMetadata:
        """Extract all metadata from article HTML."""
        return ArticleMetadata(
            title=self._extract_title(soup),
            published_date=self._extract_published_date(soup),
            tags=self._extract_tags(soup),
            meta_description=self._extract_description(soup),
            meta_image=self._extract_cover_image(soup) or "",
        )

    def _extract_article_html(self, soup: BeautifulSoup) -> str:
        """Extract and clean article HTML content."""
        container = self._find_article_container(soup)

        self._fix_lazy_loaded_images(container)
        self._remove_unwanted_tags(container)

        article_html = "".join(str(child) for child in container.children)
        article_html = self._clean_vue_markers(article_html)

        return article_html

    def _find_article_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Find the main article content container."""
        container = soup.select_one("div.item_view article")
        if container is None:
            container = soup.select_one("div.wrap_body")
        if container is None:
            container = soup.body or soup
        return container

    def _fix_lazy_loaded_images(self, container: BeautifulSoup) -> None:
        """Fix lazy-loaded images by moving data-src to src."""
        for img in container.find_all("img"):
            if not img.get("src"):
                data_src = img.get("data-src") or img.get("data-lazy-src")
                if data_src:
                    img["src"] = data_src

    def _remove_unwanted_tags(self, container: BeautifulSoup) -> None:
        """Remove script and style tags."""
        for tag in container.find_all(["script", "style"]):
            tag.decompose()

    def _clean_vue_markers(self, html: str) -> str:
        """Remove Vue.js framework comment markers."""
        html = re.sub(r'<!--\[-->', '', html)
        html = re.sub(r'<!--\]-->', '', html)
        html = re.sub(r'<!--\[!-->', '', html)
        html = re.sub(r'<!--\]!-->', '', html)
        html = re.sub(r'<!-- -->', '', html)
        html = re.sub(r'[\[\]!]{3,}', '', html)
        return html
