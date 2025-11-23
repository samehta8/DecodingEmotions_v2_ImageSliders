"""
Google Drive manager for video file access.
Handles connections and file operations with Google Drive.
"""
import streamlit as st
import os
import io
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import tempfile
from pathlib import Path

# Global connection cache
_gdrive_service = None

# Cache for downloaded videos (filepath -> local temp path)
_video_cache = {}

def get_gdrive_service():
    """
    Get or create a cached Google Drive service.

    Returns:
        Google Drive service object or None if connection fails
    """
    global _gdrive_service

    if _gdrive_service is None:
        try:
            # Get credentials from secrets (same service account as Google Sheets)
            credentials_dict = dict(st.secrets["connections"]["gsheets"])

            # Remove the spreadsheet URL as it's not part of credentials
            credentials_dict.pop('spreadsheet', None)

            # Create credentials object
            credentials = Credentials.from_service_account_info(
                credentials_dict,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )

            # Build the Drive service
            _gdrive_service = build('drive', 'v3', credentials=credentials)
            print("[INFO] Google Drive service initialized")

        except Exception as e:
            print(f"[ERROR] Failed to create Google Drive service: {e}")
            return None

    return _gdrive_service


def list_videos_in_folder(folder_id):
    """
    List all video files in a Google Drive folder.

    Args:
        folder_id: Google Drive folder ID

    Returns:
        List of dicts with 'id', 'name' for each video file, or empty list on error
    """
    service = get_gdrive_service()
    if not service:
        print("[ERROR] Cannot list videos - Google Drive service not available")
        return []

    try:
        # Query for video files in the folder
        query = f"'{folder_id}' in parents and (mimeType contains 'video/' or name contains '.mp4')"

        results = service.files().list(
            q=query,
            fields="files(id, name)",
            pageSize=1000  # Adjust if you have more than 1000 videos
        ).execute()

        files = results.get('files', [])
        print(f"[INFO] Found {len(files)} video files in Google Drive folder")

        return files

    except Exception as e:
        print(f"[ERROR] Failed to list videos from Google Drive: {e}")
        return []


def download_video_to_temp(file_id, filename):
    """
    Download a video file from Google Drive to a temporary location.
    Uses caching to avoid re-downloading the same file.

    Args:
        file_id: Google Drive file ID
        filename: Original filename (for cache key and extension)

    Returns:
        Path to local temporary file, or None on error
    """
    global _video_cache

    # Check cache first
    cache_key = f"{file_id}_{filename}"
    if cache_key in _video_cache:
        cached_path = _video_cache[cache_key]
        if os.path.exists(cached_path):
            print(f"[INFO] Using cached video: {filename}")
            return cached_path
        else:
            # Cache entry is stale, remove it
            del _video_cache[cache_key]

    service = get_gdrive_service()
    if not service:
        print("[ERROR] Cannot download video - Google Drive service not available")
        return None

    try:
        print(f"[INFO] Downloading video from Google Drive: {filename}")

        # Request the file
        request = service.files().get_media(fileId=file_id)

        # Create temporary file with proper extension
        suffix = Path(filename).suffix or '.mp4'
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp_path = temp_file.name

        # Download to temp file
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"[INFO] Download progress: {int(status.progress() * 100)}%")

        # Write to temp file
        fh.seek(0)
        temp_file.write(fh.read())
        temp_file.close()

        # Cache the path
        _video_cache[cache_key] = temp_path

        print(f"[INFO] Video downloaded successfully: {filename}")
        return temp_path

    except Exception as e:
        print(f"[ERROR] Failed to download video '{filename}': {e}")
        return None


def get_video_path(filename, folder_id):
    """
    Get the local path for a video file from Google Drive.
    Downloads the file if not already cached.

    Args:
        filename: Video filename (e.g., 'event_001.mp4')
        folder_id: Google Drive folder ID

    Returns:
        Local file path, or None if file not found/download failed
    """
    # List all videos in folder
    videos = list_videos_in_folder(folder_id)

    # Find matching file
    matching_file = None
    for video in videos:
        if video['name'] == filename:
            matching_file = video
            break

    if not matching_file:
        print(f"[WARNING] Video '{filename}' not found in Google Drive folder")
        return None

    # Download to temp location
    return download_video_to_temp(matching_file['id'], filename)


def clear_video_cache():
    """
    Clear the video cache and delete temporary files.
    Useful for freeing up space or forcing re-download.
    """
    global _video_cache

    for cache_key, temp_path in _video_cache.items():
        try:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                print(f"[INFO] Deleted cached video: {temp_path}")
        except Exception as e:
            print(f"[WARNING] Failed to delete cached video {temp_path}: {e}")

    _video_cache.clear()
    print("[INFO] Video cache cleared")


def get_all_video_filenames(folder_id):
    """
    Get list of all video filenames in a Google Drive folder.

    Args:
        folder_id: Google Drive folder ID

    Returns:
        List of video filenames (e.g., ['event_001.mp4', 'event_002.mp4'])
    """
    videos = list_videos_in_folder(folder_id)
    return [video['name'] for video in videos]
