"""
Daily Writing Friends (매글프) post archiver.

Exports posts via API and converts to markdown format.
"""

import json
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from .base import ArticleMetadata, get_output_dir


@dataclass
class DailyWritingPost:
    """Represents a post from Daily Writing Friends."""
    id: str
    title: str
    content: str  # HTML content
    created_at: datetime
    visibility: str
    board_id: Optional[str] = None


class DailyWritingFriendsScraper:
    """Scraper for Daily Writing Friends (매글프) posts."""

    platform = "daily-writing-friends"
    API_URL = "https://us-central1-artico-app-4f9d4.cloudfunctions.net/exportUserPosts"

    def __init__(self, token: Optional[str] = None):
        """
        Initialize scraper with API token.

        Args:
            token: API token. If not provided, reads from .env file.
        """
        self.token = token or self._load_token_from_env()
        self.output_dir = get_output_dir(self.platform)

    def _load_token_from_env(self) -> str:
        """Load token from .env file."""
        env_path = Path(__file__).parent.parent.parent / ".env"
        if not env_path.exists():
            raise FileNotFoundError(f".env file not found at {env_path}")

        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("DAILY_WRITING_FRIENDS_USER_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    # Handle case where multiple tokens might be concatenated
                    parts = token.split(".")
                    if len(parts) > 3:
                        token = ".".join(parts[:3])
                    return token

        raise ValueError("DAILY_WRITING_FRIENDS_USER_TOKEN not found in .env")

    def fetch_posts(
        self,
        start_date: str,
        end_date: str,
    ) -> List[DailyWritingPost]:
        """
        Fetch posts from API for a date range.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            List of DailyWritingPost objects (only public posts)
        """
        result = subprocess.run(
            [
                "curl", "-s", "-X", "POST",
                self.API_URL,
                "-H", f"Authorization: Bearer {self.token}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps({"startDate": start_date, "endDate": end_date}),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"API call failed: {result.stderr}")

        data = json.loads(result.stdout)

        if not data.get("success"):
            error_type = data.get("type", "UNKNOWN")
            error_msg = data.get("error", "Unknown error")
            raise RuntimeError(f"API error ({error_type}): {error_msg}")

        posts = []
        for post_data in data.get("posts", []):
            # Only include public posts
            if post_data.get("visibility", "").lower() != "public":
                continue

            post = DailyWritingPost(
                id=post_data["id"],
                title=post_data.get("title", "Untitled"),
                content=post_data.get("content", ""),
                created_at=datetime.fromisoformat(
                    post_data["createdAt"].replace("Z", "+00:00")
                ),
                visibility=post_data.get("visibility", ""),
                board_id=post_data.get("boardId"),
            )
            posts.append(post)

        return posts

    def fetch_all_posts(self, weeks_ago: int = 85) -> List[DailyWritingPost]:
        """
        Fetch all posts from the beginning.

        API has a 365-day limit, so we batch requests if needed.

        Args:
            weeks_ago: How many weeks back to start from (default: 85)

        Returns:
            List of all public posts
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks_ago)
        max_days = 364  # API limit is 365 days, use 364 to be safe

        all_posts = []
        current_end = end_date

        while current_end > start_date:
            current_start = max(start_date, current_end - timedelta(days=max_days))

            print(f"Fetching posts from {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}...")

            posts = self.fetch_posts(
                start_date=current_start.strftime("%Y-%m-%d"),
                end_date=current_end.strftime("%Y-%m-%d"),
            )
            all_posts.extend(posts)
            print(f"  Found {len(posts)} posts in this batch")

            current_end = current_start - timedelta(days=1)

        return all_posts

    def html_to_markdown(self, html: str) -> str:
        """
        Convert simple HTML (p, br tags) to Markdown.

        Args:
            html: HTML content string

        Returns:
            Markdown formatted string
        """
        # Replace <br> with newlines
        text = re.sub(r"<br\s*/?>", "\n", html)
        # Replace </p><p> with double newlines
        text = re.sub(r"</p>\s*<p>", "\n\n", text)
        # Remove remaining p tags
        text = re.sub(r"</?p>", "", text)
        # Clean up excessive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def create_metadata(self, post: DailyWritingPost) -> ArticleMetadata:
        """Create ArticleMetadata from a post."""
        return ArticleMetadata(
            title=post.title,
            published_date=post.created_at.strftime("%Y-%m-%d 00:00"),
            lang="ko",
        )

    def save_post(self, post: DailyWritingPost) -> Path:
        """
        Save a single post to markdown file.

        Args:
            post: DailyWritingPost to save

        Returns:
            Path to saved file
        """
        # Use post id as slug
        slug = post.id
        post_dir = self.output_dir / slug
        post_dir.mkdir(parents=True, exist_ok=True)

        # Convert content
        metadata = self.create_metadata(post)
        markdown_content = self.html_to_markdown(post.content)

        # Create full markdown with frontmatter
        full_content = metadata.to_frontmatter() + "\n\n" + markdown_content + "\n"

        # Write file
        output_path = post_dir / "article.md"
        output_path.write_text(full_content, encoding="utf-8")

        return output_path

    def archive_all(self, weeks_ago: int = 85) -> int:
        """
        Archive all posts.

        Args:
            weeks_ago: How many weeks back to start from

        Returns:
            Number of posts archived
        """
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Fetch all posts
        posts = self.fetch_all_posts(weeks_ago=weeks_ago)
        print(f"Found {len(posts)} public posts")

        # Save each post
        for i, post in enumerate(posts, 1):
            self.save_post(post)
            if i % 50 == 0:
                print(f"  Saved {i}/{len(posts)} posts...")

        print(f"Archived {len(posts)} posts to {self.output_dir}")
        return len(posts)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Archive posts from Daily Writing Friends (매글프)"
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=85,
        help="How many weeks back to fetch (default: 85)",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date (YYYY-MM-DD). Overrides --weeks if provided.",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date (YYYY-MM-DD). Default: today",
    )

    args = parser.parse_args()

    scraper = DailyWritingFriendsScraper()

    if args.start_date:
        posts = scraper.fetch_posts(args.start_date, args.end_date)
        print(f"Found {len(posts)} public posts")
        for post in posts:
            scraper.save_post(post)
        print(f"Archived {len(posts)} posts")
    else:
        scraper.archive_all(weeks_ago=args.weeks)


if __name__ == "__main__":
    main()
