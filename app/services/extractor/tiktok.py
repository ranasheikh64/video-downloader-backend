from app.services.extractor.base import BaseExtractor
from app.models.video import VideoInfo, VideoFormat
import yt_dlp
import traceback

class TikTokExtractor(BaseExtractor):
    # Updated yt-dlp version to fix TikTok extraction
    def extract(self) -> VideoInfo:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo+bestaudio/best', 
            'impersonate': 'chrome', # Bypasses TikTok blocking
            'extractor_args': {
                'tiktok': ['api_hostname=api16-normal-c-useast1a.tiktokv.com']
            },
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                
                title = info_dict.get('title', 'TikTok Video')
                thumbnail = info_dict.get('thumbnail')
                duration = info_dict.get('duration')
                formats = info_dict.get('formats', [])
                
                video_formats = []
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('url'):
                         quality_note = f.get('format_note') or f.get('resolution') or f.get('height')
                         if not quality_note:
                             quality_note = 'SD'
                         elif isinstance(quality_note, int):
                             quality_note = f"{quality_note}p"
                             
                         video_formats.append(
                             VideoFormat(
                                 quality=str(quality_note),
                                 resolution=str(f.get('height', 'unknown')) + 'p',
                                 url=f.get('url'),
                                 ext=f.get('ext', 'mp4')
                             )
                         )
                
                if not video_formats and info_dict.get('url'):
                     video_formats.append(
                         VideoFormat(
                             quality='Best',
                             resolution='unknown',
                             url=info_dict.get('url'),
                             ext=info_dict.get('ext', 'mp4')
                         )
                     )

                # Remove duplicates by URL roughly
                unique_formats = {v.url: v for v in video_formats}.values()

                return VideoInfo(
                    success=True,
                    platform="tiktok",
                    title=title,
                    thumbnail=thumbnail,
                    duration=duration,
                    formats=list(unique_formats)
                )
                
        except Exception as e:
            print(f"Extraction error (TikTok): {traceback.format_exc()}")
            return VideoInfo(
                success=False,
                platform="tiktok",
                error_message=str(e)
            )
