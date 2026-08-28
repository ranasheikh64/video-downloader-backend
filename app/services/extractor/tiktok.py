from app.services.extractor.base import BaseExtractor
from app.models.video import VideoInfo, VideoFormat
import urllib.request
import json
import traceback

class TikTokExtractor(BaseExtractor):
    def extract(self) -> VideoInfo:
        try:
            api_url = f"https://www.tikwm.com/api/?url={self.url}"
            
            req = urllib.request.Request(
                api_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
            if data.get('code') != 0:
                return VideoInfo(
                    success=False,
                    platform="tiktok",
                    error_message=data.get('msg', 'Failed to extract TikTok video')
                )
                
            video_data = data.get('data', {})
            title = video_data.get('title', 'TikTok Video')
            thumbnail = video_data.get('cover')
            duration = video_data.get('duration')
            
            formats = []
            
            # Unwatermarked video
            if video_data.get('play'):
                formats.append(VideoFormat(
                    quality='No Watermark',
                    resolution='HD',
                    url=video_data.get('play'),
                    ext='mp4'
                ))
                
            # Watermarked video
            if video_data.get('wmplay'):
                formats.append(VideoFormat(
                    quality='Watermarked',
                    resolution='SD',
                    url=video_data.get('wmplay'),
                    ext='mp4'
                ))
                
            # Audio
            if video_data.get('music'):
                formats.append(VideoFormat(
                    quality='Audio',
                    resolution='Audio',
                    url=video_data.get('music'),
                    ext='mp3'
                ))
                
            if not formats:
                raise ValueError("No video formats found")
                
            return VideoInfo(
                success=True,
                platform="tiktok",
                title=title,
                thumbnail=thumbnail,
                duration=duration,
                formats=formats
            )
                
        except Exception as e:
            print(f"Extraction error (TikTok): {traceback.format_exc()}")
            return VideoInfo(
                success=False,
                platform="tiktok",
                error_message=f"Failed to fetch TikTok video: {str(e)}"
            )
