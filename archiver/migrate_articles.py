#!/usr/bin/env python3
"""
Migrate archived articles to Nextra-compatible format.
Reads from archiver/brunch_md and archiver/velog_md,
outputs to app/posts/ and public/assets/posts/
"""
import os
import re
import shutil
from pathlib import Path

# Paths relative to project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SOURCE_DIRS = [
    ('brunch_md', 'brunch'),
    ('velog_md', 'velog')
]
POSTS_OUTPUT_DIR = PROJECT_ROOT / 'content'
ASSETS_OUTPUT_DIR = PROJECT_ROOT / 'public' / 'assets' / 'posts'


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        body = match.group(2)

        # Simple YAML parsing
        frontmatter = {}
        for line in fm_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()

        return frontmatter, body
    return {}, content


def transform_frontmatter(fm: dict) -> str:
    """Convert frontmatter to Nextra format."""
    lines = ['---']

    # Title (escape quotes)
    title = fm.get('title', 'Untitled').replace('"', '\\"')
    lines.append(f'title: "{title}"')

    # Date (extract just the date part)
    date_str = fm.get('published_date', '')
    if date_str:
        date_only = date_str.split()[0]
        lines.append(f'date: {date_only}')

    # Tags (convert comma-separated to YAML array)
    tags_str = fm.get('tags', '')
    if tags_str:
        tags = [t.strip() for t in tags_str.split(',') if t.strip()]
        if tags:
            lines.append('tags:')
            for tag in tags:
                lines.append(f'  - {tag}')

    # Description
    desc = fm.get('meta_description', '')
    if desc:
        desc = desc.replace('"', '\\"').strip("'")
        lines.append(f'description: "{desc}"')

    # Cover image
    image = fm.get('meta_image', '')
    if image:
        lines.append(f'image: {image}')

    lines.append('---')
    return '\n'.join(lines)


def update_image_paths(body: str, old_dir: str, new_slug: str) -> str:
    """Update image paths to use /assets/posts/{slug}/ paths."""
    # Pattern: ![...](brunch_md/bumgeunsong-160/assets/xxx.png)
    # or: ![...](velog_md/eddy_song-rejection/assets/xxx.png)
    pattern = rf'!\[([^\]]*)\]\({re.escape(old_dir)}/assets/([^)]+)\)'
    replacement = rf'![image](/assets/posts/{new_slug}/\2)'
    return re.sub(pattern, replacement, body)


def clean_mdx_content(body: str) -> str:
    """Clean content for MDX compatibility."""
    # Convert angle-bracket URLs to plain URLs
    # <https://example.com> -> https://example.com
    body = re.sub(r'<(https?://[^>]+)>', r'\1', body)

    # Remove HTML anchor tags (keep the text content if any)
    # <a href="..." target="_blank">text</a> -> text
    body = re.sub(r'<a[^>]*>([^<]*)</a>', r'\1', body)

    # Remove empty anchor tags
    body = re.sub(r'<a[^>]*/>', '', body)

    return body


def migrate_article(source_dir: Path, article_dir: str, platform: str):
    """Migrate a single article to Nextra format."""
    article_path = source_dir / article_dir / 'article.md'
    if not article_path.exists():
        print(f"  Skipping {article_dir}: no article.md found")
        return

    # Create slug
    slug = f"{platform}-{article_dir}"

    # Read content
    content = article_path.read_text(encoding='utf-8')
    fm, body = parse_frontmatter(content)

    if not fm:
        print(f"  Skipping {article_dir}: no frontmatter found")
        return

    # Transform frontmatter
    new_frontmatter = transform_frontmatter(fm)

    # Update image paths
    old_path = f"{source_dir.name}/{article_dir}"
    body = update_image_paths(body, old_path, slug)

    # Clean content for MDX compatibility
    body = clean_mdx_content(body)

    # Combine and write MDX file
    new_content = new_frontmatter + '\n\n' + body.strip() + '\n'

    output_file = POSTS_OUTPUT_DIR / f"{slug}.mdx"
    output_file.write_text(new_content, encoding='utf-8')
    print(f"  Created: {output_file.name}")

    # Copy assets
    assets_source = source_dir / article_dir / 'assets'
    if assets_source.exists():
        assets_dest = ASSETS_OUTPUT_DIR / slug
        if assets_dest.exists():
            shutil.rmtree(assets_dest)
        shutil.copytree(assets_source, assets_dest)
        print(f"  Copied assets to: public/assets/posts/{slug}/")


def main():
    """Main migration function."""
    print("Starting migration...")
    print(f"Project root: {PROJECT_ROOT}")

    # Ensure output directories exist
    POSTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    for source_name, platform in SOURCE_DIRS:
        source_path = SCRIPT_DIR / source_name
        if not source_path.exists():
            print(f"Source directory not found: {source_path}")
            continue

        print(f"\nProcessing {source_name}...")
        for article_dir in sorted(source_path.iterdir()):
            if article_dir.is_dir():
                migrate_article(source_path, article_dir.name, platform)
                total += 1

    print(f"\nMigration complete! Processed {total} articles.")


if __name__ == '__main__':
    main()
