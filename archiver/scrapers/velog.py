"""
Velog article scraper.

Extracts articles from velog.io.
"""

import json
import re
from datetime import datetime
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Comment

from .base import ArticleMetadata, sanitize_slug
from .web_scraper import WebScraper


class VelogScraper(WebScraper):
    """Scraper for Velog articles (velog.io)."""

    platform = "velog"

    def create_slug(self, url: str) -> str:
        """
        Convert Velog URL to slug.

        Examples:
            https://velog.io/@eddy_song/rejection -> eddy_song-rejection
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
        """Extract article content from Velog HTML."""
        soup = BeautifulSoup(html, "html.parser")
        apollo_state = self._extract_apollo_state(soup)

        title = self._extract_title(soup)
        author = self._extract_author(soup)
        metadata = self._extract_metadata(soup, apollo_state)
        article_html = self._extract_article_html(soup)

        return title, author, article_html, metadata

    # ============================================================
    # Velog-specific extractors
    # ============================================================

    def _extract_apollo_state(self, soup: BeautifulSoup) -> Optional[dict]:
        """Extract Apollo GraphQL state from Velog page."""
        apollo_script = soup.find('script', string=re.compile('__APOLLO_STATE__'))
        if not apollo_script:
            return None

        script_text = apollo_script.string
        match = re.search(r'window\.__APOLLO_STATE__\s*=\s*({.*?});', script_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
        return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title."""
        title_element = soup.select_one("h1")
        if title_element:
            return title_element.get_text(strip=True)

        meta_title = soup.find("meta", property="og:title")
        if meta_title:
            return meta_title.get("content", "Untitled")

        return "Untitled"

    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract author name."""
        author_element = soup.select_one("a[href^='/@']")
        if author_element:
            username = author_element.get("href", "").replace("/@", "").split("/")[0]
            return username
        return ""

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article description from meta tags."""
        desc_element = soup.find("meta", property="og:description")
        if desc_element:
            return desc_element.get("content")

        desc_element = soup.find("meta", attrs={"name": "description"})
        if desc_element:
            return desc_element.get("content")

        return None

    def _extract_published_date(self, soup: BeautifulSoup, apollo_state: Optional[dict]) -> Optional[str]:
        """Extract and format published date from Apollo state."""
        if apollo_state:
            for key, value in apollo_state.items():
                if key.startswith('Post:') and isinstance(value, dict):
                    released_at = value.get('released_at')
                    if released_at:
                        try:
                            parsed_date = datetime.fromisoformat(released_at.replace('Z', '+00:00'))
                            return parsed_date.strftime("%Y-%m-%d %H:%M")
                        except (ValueError, AttributeError):
                            return released_at
        return None

    def _extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """Extract keyword tags."""
        tags = []
        tag_links = soup.select("a[href*='/tags/']")

        for tag_link in tag_links:
            tag = tag_link.get_text(strip=True)
            if tag and tag not in tags:
                tags.append(tag)

        return tags

    def _extract_cover_image(self, soup: BeautifulSoup, apollo_state: Optional[dict]) -> Optional[str]:
        """Extract cover image URL from Apollo state or meta tags."""
        if apollo_state:
            for key, value in apollo_state.items():
                if key.startswith('Post:') and isinstance(value, dict):
                    thumbnail = value.get('thumbnail')
                    if thumbnail:
                        return thumbnail

        og_image = soup.find('meta', property='og:image')
        if og_image:
            return og_image.get('content')

        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image:
            return twitter_image.get('content')

        return None

    def _extract_metadata(self, soup: BeautifulSoup, apollo_state: Optional[dict]) -> ArticleMetadata:
        """Extract all metadata from article HTML."""
        return ArticleMetadata(
            title=self._extract_title(soup),
            published_date=self._extract_published_date(soup, apollo_state),
            tags=self._extract_tags(soup),
            meta_description=self._extract_description(soup),
            meta_image=self._extract_cover_image(soup, apollo_state) or "",
        )

    def _extract_article_html(self, soup: BeautifulSoup) -> str:
        """Extract and clean article HTML content."""
        container = self._find_article_container(soup)

        if container:
            self._remove_framework_artifacts(container)
            self._remove_unwanted_tags(container)
            return "".join(str(child) for child in container.children)
        else:
            print("Warning: Could not find article container, using fallback")
            return str(soup.body) if soup.body else str(soup)

    def _find_article_container(self, soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """Find the main article content container."""
        content_divs = soup.find_all('div', class_=re.compile(r'.*'))

        for div in content_divs:
            paragraphs = div.find_all('p', recursive=False)
            if len(paragraphs) >= 3:
                div_classes = div.get('class', [])
                div_class_str = ' '.join(div_classes) if div_classes else ''

                if 'atom-one' in div_class_str or 'github' in div_class_str or 'monokai' in div_class_str:
                    return div

        return None

    def _remove_framework_artifacts(self, container: BeautifulSoup) -> None:
        """Remove React/framework artifacts."""
        for comment in container.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        for script in container.find_all('script'):
            script_text = script.string or ''
            if any(marker in script_text for marker in ['__APOLLO_STATE__', '__REDUX_STATE__', '__NEXT_DATA__']):
                script.extract()

    def _remove_unwanted_tags(self, container: BeautifulSoup) -> None:
        """Remove script and style tags."""
        for tag in container.find_all(["script", "style"]):
            tag.decompose()
