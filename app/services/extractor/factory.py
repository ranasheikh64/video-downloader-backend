from app.services.extractor.base import BaseExtractor
from app.services.extractor.facebook import FacebookExtractor
from urllib.parse import urlparse

class ExtractorFactory:
    @staticmethod
    def get_extractor(url: str) -> BaseExtractor:
        domain = urlparse(url).netloc.lower()
        if 'facebook.com' in domain or 'fb.watch' in domain or 'fb.gg' in domain:
            return FacebookExtractor(url)
        # Add more extractors here for tiktok, instagram, etc.
        raise ValueError(f"Platform not supported for URL: {url}")
