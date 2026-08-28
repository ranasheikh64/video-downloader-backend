# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import List, Optional

class VideoFormat(BaseModel):
    quality: str    
    resolution: str
    url: str
    ext: str

class VideoInfo(BaseModel):
    success: bool
    platform: str
    title: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[float] = None
    formats: List[VideoFormat] = []
    error_message: Optional[str] = None
