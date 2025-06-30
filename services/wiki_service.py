import os
import uuid
from contextlib import closing
from datetime import datetime

from config import UPLOAD_DIR
from db import get_db_connection
from models import WikiInstance


class WikiService:
    def create_wiki(self, title, description, category, icon=None):
        wiki_id = str(uuid.uuid4())
        icon_filename = None

        # Handle icon upload
        if icon and icon.file:
            upload_dir = os.path.join(UPLOAD_DIR, "wikis", wiki_id)
            os.makedirs(upload_dir, exist_ok=True)
            icon_filename = (
                f"icon_{int(datetime.now().timestamp())}.{icon.filename.split('.')[-1]}"
            )
            icon.save(os.path.join(upload_dir, icon_filename))

        # Save to database
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO wikis (id, title, description, category, icon) "
                "VALUES (?, ?, ?, ?, ?)",
                (wiki_id, title, description, category, icon_filename),
            )
            conn.commit()

        return WikiInstance(
            id=wiki_id,
            title=title,
            description=description,
            category=category,
            icon=icon_filename,
        )

    def get_wiki(self, wiki_id):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wikis WHERE id = ?", (wiki_id,))
            wiki_data = cursor.fetchone()

            if not wiki_data:
                return None

            return WikiInstance(
                id=wiki_data["id"],
                title=wiki_data["title"],
                description=wiki_data["description"],
                category=wiki_data["category"],
                icon=wiki_data["icon"],
                created_at=wiki_data["created_at"],
                owner_id=wiki_data["owner_id"],
            )

    def get_all_wikis(self):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wikis")
            return [
                WikiInstance(
                    id=row["id"],
                    title=row["title"],
                    description=row["description"],
                    category=row["category"],
                    icon=row["icon"],
                    created_at=row["created_at"],
                )
                for row in cursor.fetchall()
            ]

    def create_page(self, wiki_id, title, content, tags):
        page_id = str(uuid.uuid4())

        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pages (id, wiki_id, title, content, tags) "
                "VALUES (?, ?, ?, ?, ?)",
                (page_id, wiki_id, title, content, ",".join(tags)),
            )
            conn.commit()

        return WikiPage(
            id=page_id, wiki_id=wiki_id, title=title, content=content, tags=tags
        )

    def get_page(self, wiki_id, page_id):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM pages WHERE id = ? AND wiki_id = ?", (page_id, wiki_id)
            )
            page_data = cursor.fetchone()

            if not page_data:
                return None

            return WikiPage(
                id=page_data["id"],
                wiki_id=page_data["wiki_id"],
                title=page_data["title"],
                content=page_data["content"],
                tags=page_data["tags"].split(",") if page_data["tags"] else [],
                created_at=page_data["created_at"],
                updated_at=page_data["updated_at"],
                author_id=page_data["author_id"],
            )

    # Other service methods would follow similar patterns...
