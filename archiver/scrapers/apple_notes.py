"""
Apple Notes scraper for extracting notes from the Notes app.

Uses ScriptingBridge for fast direct access to Notes.app.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ScriptingBridge import SBApplication

try:
    from .base import ArticleMetadata
except ImportError:
    from base import ArticleMetadata


class AppleNotesScraper:
    """
    Scraper for Apple Notes app.

    Extracts notes from a specific folder and converts them to MDX format.
    Uses ScriptingBridge for optimized folder-level access.
    """

    platform: str = "apple_notes"

    def __init__(self, folder_name: str = "1일1글"):
        self.folder_name = folder_name
        self.app = SBApplication.applicationWithBundleIdentifier_("com.apple.Notes")
        self.output_dir = Path(__file__).parent.parent.parent / "content"
        self._folder = None

    def _get_folder(self):
        """Get the target folder object (cached)."""
        if self._folder is None:
            for folder in self.app.folders():
                if folder.name() == self.folder_name:
                    self._folder = folder
                    break
        return self._folder

    def find_notes(self) -> List:
        """
        Find all notes in the specified folder.

        Returns:
            List of note objects from the folder
        """
        folder = self._get_folder()
        if folder:
            return list(folder.notes())
        return []

    def clean_content(self, text: str, title: str = "") -> str:
        """
        Clean up Apple Notes content.

        Rules:
        - Remove duplicate title from first line
        - 3+ newlines -> 2 newlines
        - 1-2 newlines -> keep as is

        Args:
            text: Raw plaintext from Apple Notes
            title: Note title (to remove duplicate from first line)

        Returns:
            Cleaned text
        """
        # Remove the title from the first line (it's duplicated)
        lines = text.split('\n')
        if lines and lines[0].strip() == title:
            lines = lines[1:]
        text = '\n'.join(lines)

        # Compress 3+ newlines to 2 newlines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Trim trailing whitespace from each line
        text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)

        return text.strip()

    def create_slug(self, note) -> str:
        """
        Create a filesystem-safe slug from note ID.

        Args:
            note: Note object (ScriptingBridge)

        Returns:
            Slug string (e.g., 'p494')
        """
        note_id = note.id()
        match = re.search(r'/(\w+)$', note_id)
        return match.group(1) if match else "note"

    def extract_metadata(self, note) -> ArticleMetadata:
        """
        Extract metadata from a note.

        Args:
            note: Note object (ScriptingBridge)

        Returns:
            ArticleMetadata object
        """
        # Get first 100 chars of content as description
        content = note.plaintext() or ""
        title = note.name() or ""
        # Skip title line
        lines = content.split('\n')
        body_start = '\n'.join(lines[1:]).strip()
        description = body_start[:100].replace('\n', ' ').strip()
        if len(body_start) > 100:
            description += "..."

        # Get creation date (NSDate -> Python datetime)
        creation_date = note.creationDate()
        if creation_date:
            # Convert NSDate to Python datetime
            from Foundation import NSDate
            timestamp = creation_date.timeIntervalSince1970()
            dt = datetime.fromtimestamp(timestamp)
            date_str = dt.strftime("%Y-%m-%d")
        else:
            date_str = ""

        return ArticleMetadata(
            title=title,
            published_date=date_str,
            tags=["essay"],
            meta_description=description,
            lang="ko"
        )

    def to_frontmatter(self, metadata: ArticleMetadata, source: str) -> str:
        """
        Convert metadata to YAML frontmatter for MDX.

        Args:
            metadata: ArticleMetadata object
            source: Source identifier

        Returns:
            YAML frontmatter string
        """
        lines = ["---"]

        # Escape quotes in title
        title = metadata.title.replace('"', '\\"')
        lines.append(f'title: "{title}"')

        if metadata.published_date:
            lines.append(f"date: {metadata.published_date}")

        lines.append(f"source: {source}")

        if metadata.tags:
            lines.append("tags:")
            for tag in metadata.tags:
                lines.append(f"  - {tag}")

        if metadata.meta_description:
            desc = metadata.meta_description.replace('"', '\\"')
            lines.append(f'description: "{desc}"')

        lines.append("---")
        return "\n".join(lines)

    def transform_note(self, note, dry_run: bool = False) -> Optional[str]:
        """
        Transform a single note to MDX format.

        Args:
            note: Note object (ScriptingBridge)
            dry_run: If True, print output instead of writing file

        Returns:
            Output filename if successful, None otherwise
        """
        try:
            title = note.name() or ""
            plaintext = note.plaintext() or ""

            # Extract metadata
            metadata = self.extract_metadata(note)

            # Clean content
            content = self.clean_content(plaintext, title)

            # Create slug and filename
            slug = self.create_slug(note)
            filename = f"{self.platform}-{slug}.mdx"

            # Build full content
            frontmatter = self.to_frontmatter(metadata, self.platform)
            full_content = f"{frontmatter}\n\n{content}\n"

            if dry_run:
                print(f"=== {filename} ===")
                print(full_content)
                print("=" * 50)
                return filename

            # Write file
            output_path = self.output_dir / filename
            output_path.write_text(full_content, encoding="utf-8")

            return filename

        except Exception as e:
            print(f"Error processing note '{title}': {e}")
            return None

    def run(self, limit: int = None, dry_run: bool = False) -> None:
        """
        Process notes from the folder.

        Args:
            limit: Maximum number of notes to process (None = all)
            dry_run: If True, print output instead of writing files
        """
        print(f"Apple Notes Scraper - Folder: {self.folder_name}")
        print("=" * 50)

        notes = self.find_notes()
        print(f"Found {len(notes)} notes in '{self.folder_name}'")

        if limit:
            notes = notes[:limit]
            print(f"Processing first {limit} note(s)")

        print()

        successful = 0
        for note in notes:
            print(f"Processing: {note.name()}")
            result = self.transform_note(note, dry_run=dry_run)
            if result:
                if not dry_run:
                    print(f"  -> {result}")
                successful += 1

        print()
        print(f"Done! Processed {successful}/{len(notes)} notes.")


if __name__ == "__main__":
    scraper = AppleNotesScraper(folder_name="1일1글")
    # Test with 1 note, dry run
    scraper.run(limit=1, dry_run=True)
