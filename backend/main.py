from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse, Response
from pydantic import BaseModel, validator, HttpUrl
from typing import Optional, List, Dict, Any
import yt_dlp
import os
import tempfile
import shutil
import logging
import traceback
from urllib.parse import quote, urlparse
import aiohttp
import asyncio
import json
from datetime import datetime
import hashlib
import requests
import io
import ffmpeg
import re
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Configuration
SUPPORTED_PLATFORMS = {
    "youtube.com": "youtube",
    "youtu.be": "youtube",
    "facebook.com": "facebook",
    "fb.watch": "facebook",
    "instagram.com": "instagram",
    "twitter.com": "twitter",
    "x.com": "twitter",
    "tiktok.com": "tiktok",
    "linkedin.com": "linkedin"
}

# In-memory storage for download progress
download_progress = {}

# Add at the top of the file with other global variables
video_info_cache = {}

class VideoRequest(BaseModel):
    url: str
    format_id: Optional[str] = None
    quality: Optional[str] = None
    download_id: Optional[str] = None

    @validator('url')
    def validate_url(cls, v):
        if not v:
            raise ValueError('URL is required')
        if not any(platform in v.lower() for platform in ['youtube.com', 'youtu.be', 'facebook.com', 'instagram.com', 'tiktok.com', 'twitter.com', 'pinterest.com']):
            raise ValueError('Invalid URL. Please enter a valid video URL from YouTube, Facebook, Instagram, TikTok, Twitter, or Pinterest.')
        return v

class VideoFormat(BaseModel):
    resolution: str
    url: str
    size: Optional[str] = None
    quality: Optional[str] = None
    format_id: Optional[str] = None
    ext: Optional[str] = None

class VideoResponse(BaseModel):
    title: str
    thumbnail: Optional[str] = None
    duration: Optional[str] = None
    formats: List[VideoFormat]
    platform: str
    download_id: Optional[str] = None

class DownloadProgress(BaseModel):
    status: str
    progress: float
    speed: Optional[str] = None
    eta: Optional[str] = None
    error: Optional[str] = None

class VideoDownloadRequest(BaseModel):
    url: str
    format: str
    fileName: str = None
    compress: bool = False
    quality: int = None

def generate_download_id(url: str) -> str:
    """Generate a unique download ID based on URL and timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    return f"{timestamp}_{url_hash}"

def progress_hook(d):
    """Track download progress."""
    if d['status'] == 'downloading':
        download_id = d.get('info_dict', {}).get('download_id')
        if download_id:
            try:
                # Calculate progress percentage
                total_bytes = d.get('total_bytes', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                if total_bytes > 0:
                    progress = (downloaded_bytes / total_bytes) * 100
                else:
                    progress = 0

                # Get filename from info_dict or use a default
                filename = d.get('info_dict', {}).get('filename', 'video.mp4')
                if filename:
                    # Clean the filename to avoid URL encoding issues
                    filename = filename.split('/')[-1]  # Get just the filename part
                    filename = filename.replace(' ', '_')  # Replace spaces with underscores

                download_progress[download_id] = {
                    'status': 'downloading',
                    'progress': f"{progress:.1f}",
                    'speed': d.get('_speed_str', 'N/A'),
                    'eta': d.get('_eta_str', 'N/A'),
                    'downloaded_bytes': downloaded_bytes,
                    'total_bytes': total_bytes,
                    'filename': filename
                }
                logger.info(f"Download progress for {download_id}: {progress:.1f}%")
            except Exception as e:
                logger.error(f"Error updating progress: {str(e)}")
    elif d['status'] == 'finished':
        download_id = d.get('info_dict', {}).get('download_id')
        if download_id:
            filename = d.get('info_dict', {}).get('filename', 'video.mp4')
            if filename:
                filename = filename.split('/')[-1]
                filename = filename.replace(' ', '_')

            download_progress[download_id] = {
                'status': 'finished',
                'progress': '100',
                'speed': 'N/A',
                'eta': 'N/A',
                'filename': filename
            }
            logger.info(f"Download finished for {download_id}")

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_platform(url: str) -> str:
    """Determine the platform from the URL."""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'facebook.com' in url or 'fb.watch' in url:
        return 'facebook'
    elif 'instagram.com' in url:
        return 'instagram'
    elif 'tiktok.com' in url:
        return 'tiktok'
    else:
        raise ValueError("Unsupported platform")

async def fetch_from_rapidapi(platform: str, url: str) -> Dict:
    """Fetch video information from RapidAPI."""
    if platform not in API_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Platform {platform} not supported")
    
    api_config = API_CONFIGS[platform]
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": api_config["host"]
    }
    
    params = {"url": url}
    if platform == "youtube":
        params["format"] = "mp4"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_config["url"], headers=headers, params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"RapidAPI error for {platform}: {error_text}")
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Failed to fetch video from {platform}"
                    )
                
                data = await response.json()
                logger.info(f"RapidAPI response for {platform}: {data}")
                return data
                
        except aiohttp.ClientError as e:
            logger.error(f"RapidAPI request failed for {platform}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to {platform} service"
            )

def parse_rapidapi_response(platform: str, data: Dict) -> VideoResponse:
    """Parse RapidAPI response into our VideoResponse format."""
    try:
        if platform == "youtube":
            formats = []
            # Handle the new YouTube API response format
            if isinstance(data, dict):
                # Check for different quality options
                for quality, url in data.get("downloads", {}).items():
                    if url and isinstance(url, str):
                        formats.append(VideoFormat(
                            resolution=quality,
                            url=url,
                            quality=quality,
                            format_id=quality,
                            ext="mp4"
                        ))
                
                return VideoResponse(
                    title=data.get("title", ""),
                    thumbnail=data.get("thumbnail", ""),
                    duration=str(data.get("duration", "")),
                    formats=formats,
                    platform=platform
                )
            else:
                raise HTTPException(status_code=400, detail="Invalid response format from YouTube API")
        
        elif platform == "facebook":
            formats = []
            # Handle the new Facebook API response format
            if isinstance(data, dict):
                # Check for HD quality
                if hd_url := data.get("hd"):
                    formats.append(VideoFormat(
                        resolution="HD",
                        url=hd_url,
                        quality="HD",
                        format_id="hd",
                        ext="mp4"
                    ))
                # Check for SD quality
                if sd_url := data.get("sd"):
                    formats.append(VideoFormat(
                        resolution="SD",
                        url=sd_url,
                        quality="SD",
                        format_id="sd",
                        ext="mp4"
                    ))
                # Check for thumbnail
                thumbnail = data.get("thumb", "")
                
                return VideoResponse(
                    title=data.get("title", ""),
                    thumbnail=thumbnail,
                    formats=formats,
                    platform=platform
                )
            else:
                raise HTTPException(status_code=400, detail="Invalid response format from Facebook API")
        
        elif platform == "tiktok":
            formats = []
            for quality, url in data.get("videos", {}).items():
                formats.append(VideoFormat(
                    resolution=quality,
                    url=url,
                    quality=quality,
                    format_id=quality,
                    ext="mp4"
                ))
            
            return VideoResponse(
                title=data.get("desc", ""),
                thumbnail=data.get("cover", ""),
                formats=formats,
                platform=platform
            )
        
        elif platform == "instagram":
            formats = []
            for quality, url in data.get("videos", {}).items():
                formats.append(VideoFormat(
                    resolution=quality,
                    url=url,
                    quality=quality,
                    format_id=quality,
                    ext="mp4"
                ))
            
            return VideoResponse(
                title=data.get("title", ""),
                thumbnail=data.get("thumbnail", ""),
                formats=formats,
                platform=platform
            )
        
        raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
    except Exception as e:
        logger.error(f"Error parsing RapidAPI response: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to parse video information")

@app.get("/api/progress/{download_id}")
async def get_download_progress(download_id: str):
    """Get the progress of a download."""
    if download_id not in download_progress:
        raise HTTPException(status_code=404, detail="Download not found")
    return download_progress[download_id]

@app.post("/api/convert")
async def convert_video(request: VideoRequest):
    """Handle video conversion for all platforms."""
    try:
        platform = get_platform(request.url)
        logger.info(f"Processing convert request for platform: {platform}")

        # Use yt-dlp for all platforms
        return await convert_youtube_video(request)
            
    except HTTPException as he:
        logger.error(f"HTTP error in convert_video: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Error in convert_video: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/formats")
async def get_formats(url: str):
    """Get available formats for a video URL."""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise HTTPException(status_code=400, detail="Could not extract video information")
            
            # Define standard formats
            standard_formats = [
                {'format_id': '1080p', 'height': 1080, 'ext': 'mp4'},
                {'format_id': '720p', 'height': 720, 'ext': 'mp4'},
                {'format_id': '360p', 'height': 360, 'ext': 'mp4'},
                {'format_id': '240p', 'height': 240, 'ext': 'mp4'},
                {'format_id': '144p', 'height': 144, 'ext': 'mp4'}
            ]
            
            return {"formats": standard_formats}
            
    except Exception as e:
        logger.error(f"Error getting formats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get video formats: {str(e)}")

def compress_video(input_stream, quality):
    input_file = None
    output_file = None
    try:
        # Create temporary files with unique names
        input_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        output_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        
        # Close the files to release handles
        input_file.close()
        output_file.close()
        
        # Write input data to temporary file
        with open(input_file.name, 'wb') as f:
            f.write(input_stream.read())
        
        # Calculate bitrate based on quality
        bitrate = {
            1080: '5000k',
            720: '2500k',
            480: '1000k',
            360: '750k',
            240: '500k',
            144: '250k'
        }.get(quality, '1000k')
        
        # Run FFmpeg command
        ffmpeg.input(input_file.name).output(
            output_file.name,
            vcodec='libx264',
            acodec='aac',
            video_bitrate=bitrate,
            audio_bitrate='128k',
            preset='medium',
            movflags='faststart'
        ).overwrite_output().run(quiet=True)
        
        # Read compressed output
        with open(output_file.name, 'rb') as f:
            compressed_data = f.read()
        
        if len(compressed_data) == 0:
            raise ValueError("Compression resulted in empty file")
        
        return io.BytesIO(compressed_data)
    
    except Exception as e:
        logger.error(f"Compression error: {str(e)}")
        # Return original video if compression fails
        input_stream.seek(0)
        return input_stream
    
    finally:
        # Clean up temp files
        try:
            if input_file and os.path.exists(input_file.name):
                os.unlink(input_file.name)
            if output_file and os.path.exists(output_file.name):
                os.unlink(output_file.name)
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {str(e)}")

@app.get("/api/download-progress/{filename}")
async def get_download_progress(filename: str):
    """Get the progress of a download."""
    # Find the download_id by filename
    download_id = None
    for key, value in download_progress.items():
        if value.get('filename') == filename:
            download_id = key
            break
    
    if not download_id:
        return JSONResponse(
            status_code=404,
            content={"detail": "Download not found"}
        )
    return download_progress[download_id]

@app.post("/api/download")
async def download_video(request: Request):
    try:
        data = await request.json()
        url = data.get('url')
        format = data.get('format', 'best')
        filename = data.get('filename', 'video.mp4')
        quality = data.get('quality', 1080)
        platform = data.get('platform', 'youtube')

        if not url:
            return JSONResponse(
                status_code=400,
                content={"detail": "URL is required"}
            )

        # Generate a unique download ID
        download_id = generate_download_id(url)
        logger.info(f"Starting download with ID: {download_id}")

        # Initialize progress tracking
        download_progress[download_id] = {
            'status': 'starting',
            'progress': '0',
            'speed': 'N/A',
            'eta': 'N/A',
            'filename': filename
        }

        # Create a temporary directory for downloads
        temp_dir = Path("temp_downloads")
        temp_dir.mkdir(exist_ok=True)
        output_path = temp_dir / filename

        # Configure yt-dlp options with improved settings
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(output_path),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'force_generic_extractor': False,
            'socket_timeout': 30,
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 10,
            'extractor_retries': 10,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'prefer_insecure': True,
            'legacyserverconnect': True,
            'source_address': '0.0.0.0',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'progress_hooks': [progress_hook],
            'verbose': True,
            'logger': logger,
            'format_sort': ['res', 'fps', 'codec', 'size', 'br', 'asr', 'ext'],
            'merge_output_format': 'mp4',
            'extractor_args': {
                'youtube': {
                    'player_client': ['web'],
                    'player_skip': ['webpage', 'config', 'js'],
                    'formats': 'missing_pot'
                }
            }
        }

        # Platform-specific options
        if platform == 'youtube':
            # Define allowed qualities
            allowed_qualities = [144, 240, 360, 720, 1080]
            
            # First try to get available formats
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    if not info:
                        raise Exception("Could not extract video information")
                    
                    # Get available formats
                    formats = info.get('formats', [])
                    available_heights = [f.get('height', 0) for f in formats if f.get('height')]
                    
                    if available_heights:
                        # Find the closest allowed quality to requested quality
                        closest_height = min(allowed_qualities, key=lambda x: abs(x - quality))
                        # For YouTube Shorts, use a more flexible format selection
                        if 'shorts' in url:
                            ydl_opts['format'] = f'best[height<={closest_height}]'
                        else:
                            ydl_opts['format'] = f'bestvideo[height={closest_height}]+bestaudio/best[height={closest_height}]'
                        logger.info(f"Using closest allowed quality: {closest_height}p")
                    else:
                        # Fallback to best available format
                        ydl_opts['format'] = 'best'
                        logger.info("Using best available format")
                except Exception as e:
                    logger.warning(f"Error getting formats: {str(e)}")
                    # Fallback to default format
                    ydl_opts['format'] = 'best'

            # Add specific options for YouTube Shorts
            if 'shorts' in url:
                ydl_opts['extractor_args'] = {
                    'youtube': {
                        'player_client': ['web'],
                        'player_skip': ['webpage', 'config', 'js'],
                        'formats': 'missing_pot',
                        'skip_dash_manifest': True
                    }
                }

        elif platform == 'tiktok':
            ydl_opts['format'] = 'best'
            ydl_opts['extractor_args'] = {
                'tiktok': {
                    'download_timeout': 30,
                    'retries': 10
                }
            }
        elif platform == 'instagram':
            ydl_opts['format'] = 'best'
            ydl_opts['extractor_args'] = {
                'instagram': {
                    'download_timeout': 30,
                    'retries': 10
                }
            }

        logger.info(f"Using format: {ydl_opts['format']}")

        # Download the video with retry mechanism
        max_retries = 3
        last_error = None
        for attempt in range(max_retries):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    logger.info(f"Starting download attempt {attempt + 1} for URL: {url}")
                    
                    # First try to extract info without downloading
                    info = ydl.extract_info(url, download=False)
                    if not info:
                        raise Exception("Could not extract video information")
                    
                    logger.info(f"Video info extracted successfully: {info.get('title', 'Unknown title')}")
                    
                    # Now try to download
                    ydl.download([url])
                    
                    # Verify the downloaded file
                    if output_path.exists():
                        file_size = output_path.stat().st_size
                        if file_size > 0:
                            logger.info(f"Download successful. File size: {file_size} bytes")
                            break
                        else:
                            logger.warning(f"Downloaded file is empty (attempt {attempt + 1})")
                            output_path.unlink()  # Remove empty file
                    else:
                        logger.warning(f"Downloaded file not found (attempt {attempt + 1})")
                
                if attempt < max_retries - 1:
                    logger.info(f"Retrying download... (attempt {attempt + 2})")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    
            except Exception as e:
                last_error = str(e)
                logger.error(f"Download attempt {attempt + 1} failed: {last_error}")
                logger.error(f"Error type: {type(e).__name__}")
                logger.error(f"Error details: {traceback.format_exc()}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                continue

        # Check if file exists and is not empty after all attempts
        if not output_path.exists() or output_path.stat().st_size == 0:
            error_msg = f"Failed to download video after {max_retries} attempts"
            if last_error:
                error_msg += f": {last_error}"
            logger.error(error_msg)
            return JSONResponse(
                status_code=500,
                content={"detail": error_msg}
            )

        # Read the file and return it
        file_content = output_path.read_bytes()
        file_size = len(file_content)
        
        if file_size == 0:
            error_msg = "Downloaded file is empty"
            logger.error(error_msg)
            return JSONResponse(
                status_code=500,
                content={"detail": error_msg}
            )
            
        logger.info(f"Successfully downloaded file. Size: {file_size} bytes")
        
        # Clean up the temporary file
        output_path.unlink()

        # Return the file with proper headers
        return Response(
            content=file_content,
            media_type="video/mp4",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(file_size)
            }
        )

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": error_msg}
        )

async def convert_youtube_video(request: VideoRequest):
    """Handle YouTube video conversion using yt-dlp."""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'no_playlist': True,
            'playlist_items': '1',
            'no_download': True,
            'format_sort': ['res', 'fps', 'codec', 'size', 'br', 'asr', 'ext'],
            'merge_output_format': 'mp4',
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 10,
            'extractor_retries': 10,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'prefer_insecure': True,
            'legacyserverconnect': True,
            'source_address': '0.0.0.0',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage', 'config', 'js']
                }
            },
            'socket_timeout': 30,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=False)
            if not info:
                raise HTTPException(status_code=400, detail="Could not extract video information")

            formats = []
            if 'formats' in info:
                # Create a dictionary to store unique resolutions
                unique_formats = {}
                
                for f in info['formats']:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        height = f.get('height', 0)
                        if height and height not in unique_formats:
                            unique_formats[height] = f

                # Convert dictionary to list and sort by height
                for height, f in sorted(unique_formats.items(), reverse=True):
                    formats.append(VideoFormat(
                        resolution=f"{height}p",
                        url=f.get('url', ''),
                        size=f.get('filesize_str'),
                        quality=f"{height}p",
                        format_id=f"{height}p"  # Use resolution as format_id
                    ))

            return VideoResponse(
                title=info.get('title', ''),
                thumbnail=info.get('thumbnail', ''),
                duration=str(info.get('duration', '')),
                formats=formats,
                platform="youtube"
            )

    except Exception as e:
        logger.error(f"Error in convert_youtube_video: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

async def download_youtube_video(request: VideoDownloadRequest):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        
        ydl_opts = {
            'format': f'bestvideo[height<={request.quality}]+bestaudio/best[height<={request.quality}]',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the video
            info = ydl.extract_info(request.url, download=True)
            if not info:
                raise HTTPException(status_code=400, detail="Could not extract video information")
            
            # Get the downloaded file path
            filename = ydl.prepare_filename(info)
            if not os.path.exists(filename):
                raise HTTPException(status_code=400, detail="Downloaded file not found")
            
            # Check file size
            file_size = os.path.getsize(filename)
            if file_size == 0:
                raise HTTPException(status_code=400, detail="Downloaded file is empty")
            
            # Create safe filename with proper encoding
            safe_title = ''.join(c for c in info.get('title', '') if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')
            output_filename = request.fileName or f"{safe_title}_{request.quality}p.mp4"
            
            # Read file into memory
            with open(filename, 'rb') as f:
                video_data = f.read()
            
            if len(video_data) == 0:
                raise HTTPException(status_code=400, detail="Video data is empty")
            
            buffer = io.BytesIO(video_data)
            
            # Compress if requested
            if request.compress:
                try:
                    compressed_buffer = compress_video(buffer, request.quality)
                    if compressed_buffer.getbuffer().nbytes > 0:
                        buffer = compressed_buffer
                    else:
                        logger.warning("Compression resulted in empty file, using original")
                        buffer.seek(0)
                except Exception as e:
                    logger.error(f"Compression error: {str(e)}")
                    buffer.seek(0)
            
            # Final size check
            final_size = buffer.getbuffer().nbytes
            if final_size == 0:
                raise HTTPException(status_code=400, detail="Final video buffer is empty")
            
            # Return the video with properly encoded headers
            return StreamingResponse(
                buffer,
                media_type="video/mp4",
                headers={
                    "Content-Disposition": f'attachment; filename="{output_filename.encode("ascii", "ignore").decode("ascii")}"',
                    "Content-Type": "video/mp4",
                    "Content-Length": str(final_size)
                }
            )
            
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=f"Failed to download video: {str(e)}")
    finally:
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                logger.error(f"Error cleaning up temp directory: {str(e)}")

async def download_facebook_video(request: VideoDownloadRequest):
    """Download Facebook video using yt-dlp."""
    temp_dir = tempfile.mkdtemp()
    try:
        # First get video info without downloading
        info_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 30,
            'retries': 10,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }
        
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            try:
                # First get video info
                info = ydl.extract_info(request.url, download=False)
                if not info:
                    raise HTTPException(status_code=400, detail="Could not extract video information")
                
                # Store thumbnail and title
                thumbnail_url = info.get('thumbnail', '')
                original_title = info.get('title', '')
                
                # Create safe filename from original title
                safe_title = ''.join(c for c in original_title if c.isascii() and (c.isalnum() or c in (' ', '-', '_'))).strip()
                safe_title = safe_title.replace(' ', '_')
                if not safe_title:
                    safe_title = 'facebook_video'
                
                # Configure download options
                download_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'format': 'best',  # Always use best available format for Facebook
                    'outtmpl': {
                        'default': os.path.join(temp_dir, f"{safe_title}.%(ext)s")
                    },
                    'socket_timeout': 30,
                    'retries': 10,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                }
                
                # Download the video
                with yt_dlp.YoutubeDL(download_opts) as ydl_download:
                    info = ydl_download.extract_info(request.url, download=True)
                    filename = ydl_download.prepare_filename(info)
                    
                    if not os.path.exists(filename):
                        raise HTTPException(status_code=404, detail="Video file not found after download")
                    
                    with open(filename, 'rb') as f:
                        video_buffer = io.BytesIO(f.read())
                    
                    if request.compress:
                        video_buffer = compress_video(video_buffer, request.quality)
                    
                    # Use the safe title for the output filename
                    output_filename = f"{safe_title}.mp4"
                    
                    # Return the video with headers
                    headers = {
                        'Content-Disposition': f'attachment; filename="{quote(output_filename)}"',
                        'Content-Type': 'video/mp4',
                        'X-Video-Title': quote(original_title),
                        'X-Video-Thumbnail': quote(thumbnail_url)
                    }
                    
                    return StreamingResponse(
                        video_buffer,
                        media_type='video/mp4',
                        headers=headers
                    )
                    
            except Exception as e:
                logger.error(f"Facebook download error: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Failed to download Facebook video: {str(e)}")
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            logger.error(f"Error cleaning up temporary directory: {str(e)}")

@app.post("/api/info")
async def get_video_info(request: Request):
    try:
        data = await request.json()
        url = data.get('url')
        
        if not url:
            return JSONResponse(
                status_code=400,
                content={"detail": "URL is required"}
            )

        # Generate a unique download ID
        download_id = generate_download_id(url)
        logger.info(f"Fetching info for URL: {url} with ID: {download_id}")

        # Configure yt-dlp options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'force_generic_extractor': False,
            'socket_timeout': 30,
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 10,
            'extractor_retries': 10,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'prefer_insecure': True,
            'legacyserverconnect': True,
            'source_address': '0.0.0.0',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        # Extract video information
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise Exception("Could not extract video information")

                # Determine platform
                platform = 'youtube'  # default
                if 'tiktok.com' in url:
                    platform = 'tiktok'
                elif 'instagram.com' in url:
                    platform = 'instagram'
                elif 'facebook.com' in url:
                    platform = 'facebook'

                # Get available formats
                formats = []
                if 'formats' in info:
                    for f in info['formats']:
                        if f.get('format_note') and f.get('ext') == 'mp4':
                            formats.append({
                                'format_id': f['format_id'],
                                'ext': f['ext'],
                                'format_note': f['format_note'],
                                'filesize': f.get('filesize', 0),
                                'height': f.get('height', 0)
                            })

                # Sort formats by height (quality)
                formats.sort(key=lambda x: x['height'], reverse=True)

                # Prepare response
                response_data = {
                    'title': info.get('title', 'Unknown Title'),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'formats': formats,
                    'platform': platform,
                    'url': url,
                    'download_id': download_id
                }

                logger.info(f"Successfully extracted info for {url}")
                return JSONResponse(content=response_data)

            except Exception as e:
                error_msg = f"Error extracting video info: {str(e)}"
                logger.error(error_msg)
                logger.error(traceback.format_exc())
                return JSONResponse(
                    status_code=500,
                    content={"detail": error_msg}
                )

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": error_msg}
        )

async def update_video_info(url: str, info: dict):
    """Update video info in memory cache."""
    try:
        # Generate a unique key based on the URL
        video_id = url.split('v=')[-1] if 'v=' in url else url.split('/')[-1]
        cache_key = f"video_info_{video_id}"
        
        # Store in memory cache
        video_info_cache[cache_key] = {
            "title": info.get("title", ""),
            "thumbnail": info.get("thumbnail", ""),
            "duration": info.get("duration", ""),
            "formats": info.get("formats", []),
            "platform": info.get("platform", "unknown")
        }
        return video_info_cache[cache_key]
    except Exception as e:
        logger.error(f"Error updating video info: {str(e)}")
        return info

async def download_instagram_video(request: VideoDownloadRequest):
    """Download Instagram video using yt-dlp."""
    temp_dir = tempfile.mkdtemp()
    try:
        ydl_opts = {
            'format': request.format,  # Use the format from the request
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'progress_hooks': [progress_hook],
            'verbose': True
        }
        
        logger.info(f"Starting Instagram video download for URL: {request.url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(request.url, download=True)
                if not info:
                    raise HTTPException(status_code=400, detail="Could not extract video information")
                
                filename = ydl.prepare_filename(info)
                if not os.path.exists(filename):
                    raise HTTPException(status_code=404, detail="Video file not found after download")
                
                logger.info(f"Instagram video downloaded successfully: {filename}")
                
                with open(filename, 'rb') as f:
                    video_buffer = io.BytesIO(f.read())
                
                if request.compress:
                    logger.info("Compressing Instagram video...")
                    video_buffer = compress_video(video_buffer, request.quality)
                
                return StreamingResponse(
                    video_buffer,
                    media_type='video/mp4',
                    headers={
                        'Content-Disposition': f'attachment; filename="{quote(info["title"])}.mp4"'
                    }
                )
                
            except yt_dlp.utils.DownloadError as e:
                logger.error(f"Instagram download error: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Failed to download Instagram video: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error during Instagram download: {str(e)}")
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            logger.error(f"Error cleaning up temp directory: {str(e)}")

async def download_tiktok_video(request: VideoDownloadRequest):
    """Download TikTok video using yt-dlp."""
    temp_dir = tempfile.mkdtemp()
    try:
        ydl_opts = {
            'format': f'bestvideo[height<={request.quality}]+bestaudio/best[height<={request.quality}]',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'progress_hooks': [progress_hook],
            'verbose': True
        }
        
        logger.info(f"Starting TikTok video download for URL: {request.url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(request.url, download=True)
                if not info:
                    raise HTTPException(status_code=400, detail="Could not extract video information")
                
                filename = ydl.prepare_filename(info)
                if not os.path.exists(filename):
                    raise HTTPException(status_code=404, detail="Video file not found after download")
                
                logger.info(f"TikTok video downloaded successfully: {filename}")
                
                with open(filename, 'rb') as f:
                    video_buffer = io.BytesIO(f.read())
                
                if request.compress:
                    logger.info("Compressing TikTok video...")
                    video_buffer = compress_video(video_buffer, request.quality)
                
                return StreamingResponse(
                    video_buffer,
                    media_type='video/mp4',
                    headers={
                        'Content-Disposition': f'attachment; filename="{quote(info["title"])}.mp4"'
                    }
                )
                
            except yt_dlp.utils.DownloadError as e:
                logger.error(f"TikTok download error: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Failed to download TikTok video: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error during TikTok download: {str(e)}")
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            logger.error(f"Error cleaning up temporary directory: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    ) 