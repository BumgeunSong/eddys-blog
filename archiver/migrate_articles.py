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
    ('velog_md', 'velog'),
    ('learning_man_md', 'learning_man'),
    ('daily-writing-friends_md', 'daily-writing-friends'),
    ('instagram_md', 'instagram'),
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


def transform_frontmatter(fm: dict, source: str = '', slug: str = '') -> str:
    """Convert frontmatter to Nextra format."""
    lines = ['---']

    # Title (escape quotes and angle brackets)
    title = fm.get('title', 'Untitled').replace('"', '\\"')
    title = title.replace('<', '').replace('>', '')  # Remove angle brackets from title
    lines.append(f'title: "{title}"')

    # Date (extract just the date part)
    date_str = fm.get('published_date', '')
    if date_str:
        date_only = date_str.split()[0]
        lines.append(f'date: {date_only}')

    # Source (original publishing platform)
    if source:
        lines.append(f'source: {source}')

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
        # Remove angle brackets from description (they cause YAML parsing issues)
        desc = desc.replace('<', '').replace('>', '')
        lines.append(f'description: "{desc}"')

    # Cover image - transform ./assets/ paths to absolute paths
    image = fm.get('meta_image', '')
    if image:
        if image.startswith('./assets/') and slug:
            # Convert ./assets/xxx.png to /assets/posts/{slug}/xxx.png
            filename = image[9:]  # Remove './assets/'
            image = f'/assets/posts/{slug}/{filename}'
        lines.append(f'image: {image}')

    lines.append('---')
    return '\n'.join(lines)


def update_image_paths(body: str, old_dir: str, new_slug: str) -> str:
    """Update image paths to use /assets/posts/{slug}/ paths."""
    # Pattern 1: ![...](brunch_md/bumgeunsong-160/assets/xxx.png)
    # or: ![...](velog_md/eddy_song-rejection/assets/xxx.png)
    pattern = rf'!\[([^\]]*)\]\({re.escape(old_dir)}/assets/([^)]+)\)'
    replacement = rf'![image](/assets/posts/{new_slug}/\2)'
    body = re.sub(pattern, replacement, body)

    # Pattern 2: ![...](./assets/xxx.png) - used by learning_man
    pattern2 = r'!\[([^\]]*)\]\(\./assets/([^)]+)\)'
    replacement2 = rf'![image](/assets/posts/{new_slug}/\2)'
    body = re.sub(pattern2, replacement2, body)

    return body


def clean_instagram_content(body: str) -> str:
    """Clean Instagram-specific content."""
    # Replace Instagram's special space character (⠀) with newline
    body = body.replace('⠀', '\n')

    # Remove hashtags (e.g., #1일1글, #태그)
    body = re.sub(r'#\w+\s*', '', body)

    return body


def get_first_sentence(text: str, max_length: int = 80) -> str:
    """Extract first sentence from text, with ellipsis if too long."""
    # Remove hashtags first
    text = re.sub(r'#\w+\s*', '', text)
    # Replace special spaces
    text = text.replace('⠀', ' ')
    # Get first line/sentence
    text = text.strip()

    # Split by sentence endings
    match = re.match(r'^(.+?[.!?。])', text)
    if match:
        sentence = match.group(1).strip()
    else:
        # No sentence ending found, take first line
        sentence = text.split('\n')[0].strip()

    # Truncate if too long
    if len(sentence) > max_length:
        sentence = sentence[:max_length-3].strip() + '...'

    return sentence or 'Instagram Post'


def clean_mdx_content(body: str) -> str:
    """Clean content for MDX compatibility."""
    # Remove video file references (MDX can't handle them)
    body = re.sub(r'!\[([^\]]*)\]\([^)]*\.mp4\)', '', body)
    body = re.sub(r'!\[([^\]]*)\]\([^)]*\.mov\)', '', body)

    # Convert HTML headings to Markdown
    body = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', body, flags=re.DOTALL)
    body = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', body, flags=re.DOTALL)
    body = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', body, flags=re.DOTALL)

    # Remove empty headings
    body = re.sub(r'^#{1,3}\s*$', '', body, flags=re.MULTILINE)

    # Convert <strong> to **bold**
    body = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', body, flags=re.DOTALL)

    # Convert <em> to *italic*
    body = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', body, flags=re.DOTALL)

    # Remove <span> tags (keep content)
    body = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', body, flags=re.DOTALL)

    # Convert lists - handle <ol> and <ul> with <li> items
    def convert_list(match):
        tag = match.group(1)  # ol or ul
        content = match.group(2)
        is_ordered = tag == 'ol'
        # Extract list items
        items = re.findall(r'<li[^>]*>(.*?)</li>', content, flags=re.DOTALL)
        result = []
        for i, item in enumerate(items, 1):
            item = item.strip()
            if is_ordered:
                result.append(f"{i}. {item}")
            else:
                result.append(f"- {item}")
        return '\n' + '\n'.join(result) + '\n'

    body = re.sub(r'<(ol|ul)[^>]*>(.*?)</\1>', convert_list, body, flags=re.DOTALL)

    # Remove any remaining list tags
    body = re.sub(r'</?(?:ol|ul|li)[^>]*>', '', body)

    # Convert angle-bracket URLs to plain URLs
    # <https://example.com> -> https://example.com
    body = re.sub(r'<(https?://[^>]+)>', r'\1', body)

    # Remove HTML anchor tags (keep the text content if any)
    # <a href="..." target="_blank">text</a> -> text
    body = re.sub(r'<a[^>]*>([^<]*)</a>', r'\1', body)

    # Remove empty anchor tags
    body = re.sub(r'<a[^>]*/>', '', body)

    # Handle <[book title](url)> pattern - convert to just the link
    # <[늦깎이 천재들의 비밀](url)> -> [늦깎이 천재들의 비밀](url)
    body = re.sub(r'<(\[[^\]]+\]\([^)]+\))>', r'\1', body)

    # Escape all remaining angle brackets (after HTML conversion is done)
    # Skip already-escaped ones and markdown image syntax ![...](...)

    # Temporarily protect markdown images: ![alt](/path) or ![alt](http...)
    body = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'__IMG_PLACEHOLDER__\1__SEP__\2__END__', body)

    # Escape all < and > that aren't already escaped
    body = re.sub(r'(?<!\\)<', r'\\<', body)
    body = re.sub(r'(?<!\\)>', r'\\>', body)

    # Restore markdown images
    body = re.sub(r'__IMG_PLACEHOLDER__([^_]*)__SEP__([^_]*)__END__', r'![\1](\2)', body)

    # Clean up excessive newlines
    body = re.sub(r'\n{3,}', '\n\n', body)

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

    # Instagram-specific processing
    if platform == 'instagram':
        # Override title with first sentence from body
        fm['title'] = get_first_sentence(body)
        # Clean Instagram content (hashtags, special spaces)
        body = clean_instagram_content(body)

    # Transform frontmatter
    new_frontmatter = transform_frontmatter(fm, source=platform, slug=slug)

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
