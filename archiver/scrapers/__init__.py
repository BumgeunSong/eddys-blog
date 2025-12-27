"""
Scrapers package for extracting articles from various platforms.

Usage:
    from scrapers import BrunchScraper, VelogScraper, LearningManScraper

    scraper = BrunchScraper()
    scraper.run(['https://brunch.co.kr/@author/123'])
"""

from .brunch import BrunchScraper
from .velog import VelogScraper
from .learning_man import LearningManScraper

__all__ = [
    'BrunchScraper',
    'VelogScraper',
    'LearningManScraper',
]
