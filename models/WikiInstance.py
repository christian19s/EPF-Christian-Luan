import os
from datetime import datetime

from config import UPLOAD_DIR


class WikiInstance:
    def __init__(
        self,
        id,
        title,
        description,
        category,
        icon=None,
        created_at=None,
        owner_id=None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.icon = icon
        self.created_at = created_at or datetime.now()
        self.owner_id = owner_id
        self.pages = []

    def get_icon_url(self):
        if self.icon:
            return f"/wikis/{self.id}/uploads/{self.icon}"
        return "/static/images/default-wiki-icon.png"

    def get_upload_dir(self):
        return os.path.join(UPLOAD_DIR, "wikis", str(self.id))


class WikiPage:
    def __init__(
        self,
        id,
        wiki_id,
        title,
        content,
        created_at=None,
        updated_at=None,
        tags=None,
        creator_id=None,
    ):
        self.id = id
        self.wiki_id = wiki_id
        self.title = title
        self.content = content
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.tags = tags or []
        self.creator_id = creator_id
        self.revisions = []

    def add_revision(self, content, user_id):
        self.revisions.append(
            {"content": content, "user_id": user_id, "timestamp": datetime.now()}
        )
        self.content = content
        self.updated_at = datetime.now()

    def get_page_url(self):
        return f"/wikis/{self.wiki_id}/pages/{self.id}"

    def get_edit_url(self):
        return f"{self.get_page_url()}/edit"
