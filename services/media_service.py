import os
import sqlite3
import uuid
from contextlib import closing
from pathlib import Path

from data import get_db_connection, get_wiki_upload_path
from models.permSystem import PermissionSystem
from models.wiki import MediaItem
from static.exceptions.exceptions import (
    InvalidMediaType,
    MediaNotFound,
    UnauthorizedAccess,
)


class MediaService:
    def __init__(self, user_service):
        self.user_service = user_service

    def upload_media(self, file_upload, wiki_id, uploaded_by):
        """Handle media upload with validation"""
        if not file_upload or not file_upload.filename:
            raise ValueError("No file uploaded")

        # Validate file type
        ext = os.path.splitext(file_upload.filename)[1].lower()
        allowed_types = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".mp4")
        if ext not in allowed_types:
            raise InvalidMediaType(
                f"Invalid file type. Allowed: {', '.join(allowed_types)}"
            )

        # Validate file size
        MAX_SIZE = 20 * 1024 * 1024  # 20MB
        file_upload.file.seek(0, 2)  # Seek to end
        file_size = file_upload.file.tell()
        file_upload.file.seek(0)

        if file_size > MAX_SIZE:
            raise ValueError(f"File size exceeds {MAX_SIZE//(1024*1024)}MB limit")

        # Generate unique filename
        uuid_name = f"{uuid.uuid4().hex}{ext}"
        upload_dir = get_wiki_upload_path() / str(wiki_id)
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / uuid_name

        # Save file
        file_upload.save(str(file_path), overwrite=True)

        # Create database record
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO media 
                (uuid_filename, original_filename, mime_type, file_size, 
                 wiki_id, uploaded_by, file_path) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    uuid_name,
                    file_upload.filename,
                    file_upload.content_type,
                    file_size,
                    wiki_id,
                    uploaded_by.id,
                    f"wiki/{wiki_id}/{uuid_name}",
                ),
            )
            media_id = cursor.lastrowid
            conn.commit()

        return self.get_media_by_id(media_id)

    def delete_media(self, media_id, deleter):
        """Delete media with permission check"""
        media = self.get_media_by_id(media_id)

        # Check permissions
        if not PermissionSystem.can(deleter, PermissionSystem.EDIT_PAGE, media.wiki_id):
            raise UnauthorizedAccess("Insufficient permissions to delete media")

        # Delete physical file
        file_path = get_wiki_upload_path() / media.file_path
        if file_path.exists():
            file_path.unlink()

        # Delete database record
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            # Remove associations
            cursor.execute("DELETE FROM page_media WHERE media_id = ?", (media_id,))
            # Delete media
            cursor.execute("DELETE FROM media WHERE id = ?", (media_id,))
            conn.commit()

        return True

    def get_media_by_id(self, media_id):
        """Get media by ID"""
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM media WHERE id = ?", (media_id,))
            row = cursor.fetchone()
            if not row:
                raise MediaNotFound(f"Media with ID {media_id} not found")

            return MediaItem(
                id=row["id"],
                uuid_filename=row["uuid_filename"],
                original_filename=row["original_filename"],
                mime_type=row["mime_type"],
                file_size=row["file_size"],
                wiki_id=row["wiki_id"],
                uploaded_by=row["uploaded_by"],
                uploaded_at=row["uploaded_at"],
                file_path=row["file_path"],
            )

    def get_media_by_filename(self, wiki_id, filename):
        """Get media by filename"""
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM media WHERE wiki_id = ? AND uuid_filename = ?",
                (wiki_id, filename),
            )
            row = cursor.fetchone()
            if not row:
                raise MediaNotFound(f"File {filename} not found in wiki {wiki_id}")

            return MediaItem(
                id=row["id"],
                uuid_filename=row["uuid_filename"],
                original_filename=row["original_filename"],
                mime_type=row["mime_type"],
                file_size=row["file_size"],
                wiki_id=row["wiki_id"],
                uploaded_by=row["uploaded_by"],
                uploaded_at=row["uploaded_at"],
                file_path=row["file_path"],
            )

    def get_page_media(self, page_id):
        """Get media associated with a page"""
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT m.id, m.uuid_filename, m.original_filename, 
                m.mime_type, m.file_size, m.wiki_id, m.uploaded_by, 
                m.uploaded_at, m.file_path 
                FROM media m
                JOIN page_media pm ON pm.media_id = m.id
                WHERE pm.page_id = ?""",
                (page_id,),
            )
            return [
                MediaItem(
                    id=row["id"],
                    uuid_filename=row["uuid_filename"],
                    original_filename=row["original_filename"],
                    mime_type=row["mime_type"],
                    file_size=row["file_size"],
                    wiki_id=row["wiki_id"],
                    uploaded_by=row["uploaded_by"],
                    uploaded_at=row["uploaded_at"],
                    file_path=row["file_path"],
                )
                for row in cursor.fetchall()
            ]
