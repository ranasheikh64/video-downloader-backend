from abc import ABC, abstractmethod
from app.models.video import VideoInfo

class BaseExtractor(ABC):
    def __init__(self, url: str):
        self.url = url
    
    @abstractmethod
    def extract(self) -> VideoInfo:
        pass
