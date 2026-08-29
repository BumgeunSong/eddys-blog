"""
LinkedIn scraper for the "Download my data" export archive.

The export is a folder of CSVs plus an ``Articles/Articles/`` folder of HTML.
Two kinds of writing live in there and they need completely different handling:

- Feed posts (``Shares_*.csv``) -- plain text in the ``ShareCommentary`` column.
- Articles (``Articles/Articles/*.html``) -- long-form LinkedIn Pulse posts.

Both are written to ``archiver/linkedin_md/<slug>/article.md`` in the same
intermediate format the other scrapers use, so ``migrate_articles.py`` does the
final MDX conversion.

The input is the *unzipped* export folder, not the .zip itself -- the scraper
globs it for ``Shares_*.csv``. Worth double-checking what you point it at: the
download may already arrive expanded into a directory whose name still ends in
``.zip``.

Usage:
    python scrape.py linkedin /path/to/Complete_LinkedInDataExport_MM-DD-YYYY
"""

import csv
import html
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import requests

try:
    from .base import ArticleMetadata, get_output_dir
except ImportError:
    from base import ArticleMetadata, get_output_dir


# LinkedIn's export lets a field grow well past the csv module's default limit.
csv.field_size_limit(10 ** 7)

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

def is_reaction(text: str) -> bool:
    """
    True for a one-off reaction rather than a piece of writing.

    Length is a bad proxy -- "링크드인 iOS 앱 쓰시는 분들, 스크롤 빨리 하면 심하게
    버벅거리는 것(프레임 드랍) 저만 그런가요..?" is 59 characters of pure reaction,
    while a 96-character post about moving offices has a real setup and payoff.

    What separates them is structure: a reaction is a single thought dashed off
    in one paragraph, while anything the author built as a post carries at
    least one paragraph break. That split is exact over the current export --
    every single-paragraph post is a reaction, every multi-paragraph one isn't.
    """
    paragraphs = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
    return len(paragraphs) < 2


def unescape_share_commentary(raw: str) -> str:
    """
    Repair LinkedIn's broken CSV quoting in the ``ShareCommentary`` column.

    The exporter closes and reopens the CSV quote around *every* newline, so a
    paragraph break arrives as ``"\\n""\\n"`` and a plain line break as
    ``"\\n"``. Quotes the author actually typed are left un-escaped, which rules
    out any fix that strips quotes globally.

    The rule that round-trips every post: drop at most one ``"`` on each side of
    each newline, leaving every other quote alone.

        '끝났습니다."\\n""\\n"그런데'  ->  '끝났습니다.\\n\\n그런데'
        '?"\\n"왜'                   ->  '?\\n왜'    (the '?' quote is the author's)
    """
    return re.sub('"?\n"?', '\n', raw).strip()


def first_sentence(text: str, max_length: int = 80) -> str:
    """
    Derive a title from the opening sentence.

    Feed posts have no title of their own, so the listing needs one built from
    the body -- the same trick the Instagram import uses.
    """
    text = text.strip()
    # The closing quote/bracket has to come along, or a post that opens with
    # dialogue ("스포트라이트를 받고 싶었던 것 아닌가요?") is titled with a dangling
    # opening quote.
    match = re.match(r'^(.+?[.!?。?!]["\'”’」』\)]*)', text, re.DOTALL)
    sentence = match.group(1).strip() if match else text.split('\n')[0].strip()
    sentence = re.sub(r'\s+', ' ', sentence)

    if len(sentence) > max_length:
        sentence = sentence[:max_length - 3].rstrip() + '...'

    return sentence or 'LinkedIn Post'


def build_description(text: str, max_length: int = 150) -> str:
    """Flatten the opening of a post into a one-line meta description."""
    flat = re.sub(r'\s+', ' ', text).strip()
    if len(flat) > max_length:
        flat = flat[:max_length - 3].rstrip() + '...'
    return flat


class LinkedInScraper:
    """
    LinkedIn data-export scraper.

    Reads an unzipped "Download my data" archive and emits one
    ``linkedin_md/<slug>/article.md`` per feed post and per published article.
    """

    platform: str = "linkedin"

    def __init__(self, export_dir: str):
        self.export_dir = Path(export_dir).expanduser()
        self.output_dir = get_output_dir(self.platform)

    # ============================================================
    # Feed posts (Shares_*.csv)
    # ============================================================

    def find_shares_csv(self) -> Optional[Path]:
        """Locate ``Shares_<memberid>.csv``; the member id varies per account."""
        matches = sorted(self.export_dir.glob('Shares_*.csv'))
        return matches[0] if matches else None

    def parse_shares(self) -> List[Tuple[str, ArticleMetadata, str]]:
        """
        Read every original feed post from the shares CSV.

        Pure reposts are not in this file at all -- LinkedIn puts them in
        ``InstantReposts_*.csv`` with no text -- so everything here is original
        writing. Only reactions get filtered out (see ``is_reaction``).

        Returns:
            List of (slug, metadata, body) tuples
        """
        shares_csv = self.find_shares_csv()
        if not shares_csv:
            print(f"  No Shares_*.csv found in {self.export_dir}")
            return []

        posts = []
        skipped = 0

        with open(shares_csv, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                body = unescape_share_commentary(row.get('ShareCommentary', ''))

                if not body or is_reaction(body):
                    skipped += 1
                    continue

                published_at = datetime.strptime(
                    row['Date'].strip(), '%Y-%m-%d %H:%M:%S'
                )

                # Date + time, matching the instagram-YYYYMMDD-HHMMSS
                # convention. Several posts share a date, so the time is what
                # keeps the slug unique.
                slug = f"{published_at:%Y%m%d-%H%M%S}"

                metadata = ArticleMetadata(
                    title=first_sentence(body),
                    published_date=f"{published_at:%Y-%m-%d}",
                    tags=[],
                    meta_description=build_description(body),
                    lang="ko",
                )

                # A shared link isn't in the body text, so append it or it's lost.
                shared_url = row.get('SharedUrl', '').strip()
                if shared_url and shared_url not in body:
                    body = f"{body}\n\n{shared_url}"

                posts.append((slug, metadata, body))

        print(f"  Found {len(posts)} feed posts ({skipped} reactions skipped)")
        return posts

    # ============================================================
    # Articles (Articles/Articles/*.html)
    # ============================================================

    def find_article_files(self) -> List[Path]:
        """Locate the exported article HTML files."""
        articles_dir = self.export_dir / 'Articles' / 'Articles'
        if not articles_dir.exists():
            return []
        return sorted(articles_dir.glob('*.html'))

    def parse_article(
        self, path: Path
    ) -> Optional[Tuple[str, ArticleMetadata, str, str]]:
        """
        Convert one exported article HTML into markdown.

        Unpublished drafts are skipped: LinkedIn exports them alongside the real
        thing (as "Copy of ..." with ``Published on ---``), and they duplicate
        an article that was actually published.

        Returns:
            (slug, metadata, body, article_url) tuple, or None if skipped
        """
        raw = path.read_text(encoding='utf-8')

        published_match = re.search(
            r'<p class="published">Published on ([^<]+)</p>', raw
        )
        published_raw = published_match.group(1).strip() if published_match else '---'
        if published_raw == '---':
            print(f"  Skipping unpublished draft: {path.name}")
            return None

        published_date = published_raw.split()[0]

        # The <h1> wraps the canonical Pulse URL, whose trailing token is a
        # stable per-article id -- the only ASCII handle the export offers.
        title_match = re.search(
            r'<h1>\s*(?:<a href="([^"]+)">)?(.*?)(?:</a>)?\s*</h1>', raw, re.DOTALL
        )
        article_url = (title_match.group(1) or '').strip() if title_match else ''
        title = html.unescape(re.sub(r'<[^>]+>', '', title_match.group(2))).strip()

        url_id = article_url.rstrip('/').rsplit('-', 1)[-1] if article_url else path.stem
        slug = f"article-{url_id}"

        # Body is the single <div> after the created/published lines.
        body_match = re.search(r'<div>(.*)</div>\s*</body>', raw, re.DOTALL)
        if not body_match:
            print(f"  Skipping {path.name}: no article body found")
            return None
        body_html = body_match.group(1)

        markdown = self._html_to_markdown(body_html)

        first_para = re.sub(r'[#>*`\[\]!]', '', markdown.split('\n\n')[0])

        metadata = ArticleMetadata(
            title=title,
            published_date=published_date,
            tags=[],
            meta_description=build_description(first_para),
            lang="ko",
        )

        return slug, metadata, markdown, article_url

    def _html_to_markdown(self, body_html: str) -> str:
        """Run pandoc over the article body and tidy the result."""
        # Unwrap <figure>: pandoc passes it through as raw HTML, which would
        # hide the <img> from the markdown image regex in localize_images().
        # A bare <img> becomes a normal ![](url) instead.
        body_html = re.sub(r'</?figure[^>]*>', '', body_html)
        body_html = re.sub(
            r'<figcaption[^>]*>(.*?)</figcaption>', r'\1', body_html, flags=re.DOTALL
        )

        # Strip LinkedIn's data-media-urn and friends. pandoc's gfm writer falls
        # back to raw <img> HTML for any attribute it can't express in markdown,
        # and raw HTML would survive into the MDX untouched.
        body_html = re.sub(
            r'<img\b[^>]*?\bsrc="([^"]+)"[^>]*?/?>',
            lambda m: f'<img src="{m.group(1)}" />',
            body_html,
        )

        result = subprocess.run(
            ['pandoc', '-f', 'html', '-t', 'gfm', '--wrap=none'],
            input=body_html,
            capture_output=True,
            text=True,
            check=True,
        )
        markdown = result.stdout

        # pandoc keeps LinkedIn's empty <p></p> spacers as stray backslashes.
        markdown = re.sub(r'^\\\s*$', '', markdown, flags=re.MULTILINE)
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)

        return markdown.strip()

    # ============================================================
    # Images
    # ============================================================

    def _download(self, url: str, dest: Path) -> bool:
        """Fetch a remote asset, returning False rather than raising on failure."""
        try:
            response = requests.get(
                url, headers={'User-Agent': BROWSER_UA}, timeout=30
            )
            response.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(response.content)
            return True
        except Exception as exc:
            print(f"    Failed to download {url[:70]}...: {exc}")
            return False

    def fetch_cover_image(self, article_url: str, assets_dir: Path) -> str:
        """
        Download an article's cover image.

        The export's own cover ``<img src>`` is a truncated stub that 404s, so
        the real URL has to come from the live Pulse page's ``og:image``.

        Returns:
            ``./assets/<filename>`` reference, or '' when unavailable
        """
        if not article_url:
            return ''

        try:
            response = requests.get(
                article_url, headers={'User-Agent': BROWSER_UA}, timeout=30
            )
            response.raise_for_status()
            page = response.text
        except Exception as exc:
            print(f"    Could not load article page for cover: {exc}")
            return ''

        og_match = re.search(
            r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', page
        ) or re.search(
            r'og:image"\s+content="([^"]+)"', page
        )
        if not og_match:
            return ''

        cover_url = html.unescape(og_match.group(1))
        filename = 'cover.jpg'
        if self._download(cover_url, assets_dir / filename):
            return f'./assets/{filename}'
        return ''

    def localize_images(self, markdown: str, assets_dir: Path) -> str:
        """
        Download inline article images and repoint the markdown at them.

        LinkedIn's media URLs carry a signed ``e=`` expiry, so leaving them in
        would break the post within months.
        """
        def replace(match):
            alt, url = match.group(1), match.group(2)
            if not url.startswith('http'):
                return match.group(0)

            stem = re.sub(r'[^A-Za-z0-9]', '', url.split('/')[-1].split('?')[0])[:24]
            filename = f"inline-{stem or 'image'}.jpg"

            if self._download(url, assets_dir / filename):
                return f'![{alt}](./assets/{filename})'
            return ''

        return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace, markdown)

    # ============================================================
    # Output
    # ============================================================

    def write_article(
        self,
        slug: str,
        metadata: ArticleMetadata,
        body: str,
        dry_run: bool = False,
    ) -> str:
        """Write one ``linkedin_md/<slug>/article.md`` in the intermediate format."""
        content = f"{metadata.to_frontmatter()}\n\n{body}\n"

        if dry_run:
            print(f"=== {slug}/article.md ===")
            print(content[:800])
            print("=" * 50)
            return slug

        article_dir = self.output_dir / slug
        article_dir.mkdir(parents=True, exist_ok=True)
        (article_dir / 'article.md').write_text(content, encoding='utf-8')
        return slug

    def run(self, dry_run: bool = False) -> None:
        """Process the whole export: feed posts first, then articles."""
        print(f"LinkedIn Scraper - Export: {self.export_dir}")
        print("=" * 50)

        if not self.export_dir.exists():
            print(f"Export directory not found: {self.export_dir}")
            return

        print("\nParsing feed posts...")
        for slug, metadata, body in self.parse_shares():
            self.write_article(slug, metadata, body, dry_run=dry_run)
            if not dry_run:
                print(f"  -> {slug}")

        print("\nParsing articles...")
        for path in self.find_article_files():
            parsed = self.parse_article(path)
            if not parsed:
                continue

            slug, metadata, body, article_url = parsed
            assets_dir = self.output_dir / slug / 'assets'

            if not dry_run:
                body = self.localize_images(body, assets_dir)
                metadata.meta_image = self.fetch_cover_image(article_url, assets_dir)

            self.write_article(slug, metadata, body, dry_run=dry_run)
            if not dry_run:
                print(f"  -> {slug}")

        print(f"\nDone! Output: {self.output_dir}")


if __name__ == "__main__":
    export = sys.argv[1] if len(sys.argv) > 1 else "."
    LinkedInScraper(export).run(dry_run="--dry-run" in sys.argv)
