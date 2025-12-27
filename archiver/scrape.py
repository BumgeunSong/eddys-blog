#!/usr/bin/env python3
"""
Unified CLI for article scrapers.

Usage:
    # Web scrapers
    python scrape.py brunch https://brunch.co.kr/@author/123
    python scrape.py brunch urls.txt
    python scrape.py velog https://velog.io/@author/post

    # Local scrapers
    python scrape.py learning_man

    # List available platforms
    python scrape.py --list
"""

import argparse
import sys

from scrapers import BrunchScraper, VelogScraper, LearningManScraper


# Registry of available scrapers
SCRAPERS = {
    'brunch': BrunchScraper,
    'velog': VelogScraper,
    'learning_man': LearningManScraper,
}


def list_platforms():
    """List all available platforms."""
    print("Available platforms:")
    print()
    for name, scraper_class in SCRAPERS.items():
        print(f"  {name:15} - {scraper_class.__doc__.strip().split(chr(10))[0]}")
    print()
    print("Usage:")
    print("  python scrape.py <platform> [urls...]")
    print()
    print("Examples:")
    print("  python scrape.py brunch https://brunch.co.kr/@author/123")
    print("  python scrape.py brunch urls.txt")
    print("  python scrape.py learning_man")


def main():
    parser = argparse.ArgumentParser(
        description="Extract articles from various platforms.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrape.py brunch https://brunch.co.kr/@author/123
  python scrape.py brunch urls.txt
  python scrape.py velog https://velog.io/@author/post
  python scrape.py learning_man
  python scrape.py --list
        """
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available platforms'
    )
    parser.add_argument(
        'platform',
        nargs='?',
        choices=list(SCRAPERS.keys()),
        help='Platform to scrape from'
    )
    parser.add_argument(
        'urls',
        nargs='*',
        help='URLs to scrape (or path to file with URLs)'
    )

    args = parser.parse_args()

    # Handle --list
    if args.list:
        list_platforms()
        return

    # Require platform
    if not args.platform:
        parser.print_help()
        sys.exit(1)

    # Get scraper class
    scraper_class = SCRAPERS[args.platform]
    scraper = scraper_class()

    # Run scraper
    scraper.run(args.urls)


if __name__ == '__main__':
    main()
