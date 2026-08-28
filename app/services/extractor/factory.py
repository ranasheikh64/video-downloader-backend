from app.services.extractor.base import BaseExtractor
from app.services.extractor.facebook import FacebookExtractor
from app.services.extractor.tiktok import TikTokExtractor
from app.services.extractor.instagram import InstagramExtractor
from urllib.parse import urlparse

class ExtractorFactory:
    @staticmethod
    def get_extractor(url: str) -> BaseExtractor:
        domain = urlparse(url).netloc.lower()
        if 'facebook.com' in domain or 'fb.watch' in domain or 'fb.gg' in domain:
            return FacebookExtractor(url)
        elif 'tiktok.com' in domain or 'iesdouyin.com' in domain:
            return TikTokExtractor(url)
        elif 'instagram.com' in domain:
            return InstagramExtractor(url)
        raise ValueError(f"Platform not supported for URL: {url}")
