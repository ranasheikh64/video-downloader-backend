from app.services.extractor.base import BaseExtractor
from app.models.video import VideoInfo, VideoFormat
import yt_dlp
import traceback

class FacebookExtractor(BaseExtractor):
    def extract(self) -> VideoInfo:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo+bestaudio/best', # default best, but we will extract formats manually
            # Facebook specific workarounds can be added here if needed by yt-dlp
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                
                title = info_dict.get('title', 'Facebook Video')
                thumbnail = info_dict.get('thumbnail')
                duration = info_dict.get('duration')
                formats = info_dict.get('formats', [])
                
                video_formats = []
                for f in formats:
                    # Require BOTH video and audio to avoid silent DASH streams
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                         height = f.get('height')
                         format_id = f.get('format_id', '').lower()
                         format_note = f.get('format_note', '')
                         
                         if height:
                             quality = f"{height}p"
                         elif 'hd' in format_id or 'hd' in format_note.lower():
                             quality = 'HD'
                         elif 'sd' in format_id or 'sd' in format_note.lower():
                             quality = 'SD'
                         else:
                             quality = format_note if format_note else 'Normal'
                             
                         # Clean up quality string
                         if 'DASH' in quality:
                             continue # Skip DASH if it somehow slipped through
                             
                         video_formats.append(
                             VideoFormat(
                                 quality=str(quality),
                                 resolution=str(height) + 'p' if height else 'unknown',
                                 url=f.get('url'),
                                 ext=f.get('ext', 'mp4')
                             )
                         )
                
                # If we couldn't find pre-merged formats nicely, let's just add the 'best' url that yt-dlp determines
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
                    platform="facebook",
                    title=title,
                    thumbnail=thumbnail,
                    duration=duration,
                    formats=list(unique_formats)
                )
                
        except Exception as e:
            print(f"Extraction error: {traceback.format_exc()}")
            return VideoInfo(
                success=False,
                platform="facebook",
                error_message=str(e)
            )
