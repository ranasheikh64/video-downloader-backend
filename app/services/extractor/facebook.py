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
                    # Filter out formats that don't have video or are just audio (unless we want to support audio only later)
                    if f.get('vcodec') != 'none' and f.get('url'):
                         # Many platforms return separate video/audio streams. 
                         # yt-dlp provides 'format_id' and 'format_note' which helps in identifying quality.
                         # For a simple downloader, we try to find formats that have both video and audio, or fallback to video-only if we plan to merge later.
                         # Since we are not doing FFmpeg merging in backend phase 1, let's try to get pre-merged formats (acodec != 'none')
                         
                         quality_note = f.get('format_note') or f.get('resolution') or f.get('height')
                         if not quality_note:
                             quality_note = 'SD'
                         elif isinstance(quality_note, int):
                             quality_note = f"{quality_note}p"
                             
                         # basic heuristic: if acodec is none, it's video without sound
                         # for now let's just include ones with both, or if the platform only provides separated streams, 
                         # we might need to rely on the 'url' that yt-dlp resolves for 'best'
                         
                         video_formats.append(
                             VideoFormat(
                                 quality=str(quality_note),
                                 resolution=str(f.get('height', 'unknown')) + 'p',
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
