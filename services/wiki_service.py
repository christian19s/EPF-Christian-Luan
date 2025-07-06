import datetime
import os
import sqlite3
import uuid
from contextlib import closing

from bottle import HTTPResponse
from markdown import markdown

from data import get_db_connection, get_wiki_upload_path
from models.permSystem import PermissionSystem
from models.user import AuthUser
from models.wiki import MediaItem, WikiInstance, WikiPage, WikiSystem
from static.exceptions.exceptions import (InvalidMediaType, MediaNotFound,
                                          PageNotFound, UnauthorizedAccess,
                                          WikiNotFound)


class WikiService:
    def __init__(self, user_service):
        self.user_service = user_service
        self.wiki_system = WikiSystem()

    ###########################################################################
    # Wiki Operations
    ###########################################################################
    def create_wiki(self, name, slug, description, owner, category_id=None):
        if not isinstance(owner, AuthUser):
            owner = self.user_service.get_user_by_id(owner)
        
        if not PermissionSystem.can(owner, PermissionSystem.CREATE_WIKI):
            raise UnauthorizedAccess("User is not allowed to create wiki")
        
        # Validate category if provided
        if category_id is not None:
            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM categories WHERE id = ?", (category_id,))
                if not cursor.fetchone():
                    raise ValueError(f"Invalid category ID: {category_id}")
        
        # Create the wiki instance with category
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO wikis 
                (name, slug, description, owner_id, created_at, category_id) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (name, slug, description, owner.id, created_at, category_id)
            )         
            wiki_id = cursor.lastrowid
            conn.commit()
        
        # Return the created wiki instance
        return WikiInstance(
            id=wiki_id,
            name=name,
            slug=slug,
            description=description,
            owner_id=owner.id,
            created_at=created_at,
            owner_username=owner.username,
            category_id=category_id
        )

    def get_wiki_by_slug(self, slug):
        """Get wiki by slug with owner and description"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT w.id, w.name, w.slug, w.owner_id, w.created_at, w.description, 
                       w.category_id, c.name AS category_name, u.username
                FROM wikis w
                JOIN users u ON w.owner_id = u.id
                LEFT JOIN categories c ON w.category_id = c.id
                WHERE w.slug = ?
            """, (slug,))      
            row = cursor.fetchone()
            if not row:
                raise WikiNotFound(f"Wiki with slug '{slug}' not found")
        
            return WikiInstance(
                id=row[0],
                name=row[1],
                slug=row[2],
                owner_id=row[3],
                created_at=row[4],
                description=row[5] or "", 
                owner_username=row[6],
                category_id = row["category_id"],
                category_name=row["category_name"]
            )

    def update_wiki(self, wiki, updater):
        if not PermissionSystem.can(updater, PermissionSystem.MANAGE_WIKI, wiki.id):
            raise UnauthorizedAccess("Insufficient permissions to edit wiki")
            
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE wikis SET name = ?, slug = ? WHERE id = ?",
                (wiki.name, wiki.slug, wiki.id),
            )
            conn.commit()
        return True

    def delete_wiki(self, wiki_id, deleter):
        """deleta uma wiki inteira"""
        wiki = self.get_wiki_by_id(wiki_id)
        
        if not PermissionSystem.can(deleter, PermissionSystem.MANAGE_WIKI, wiki.id):
            raise UnauthorizedAccess("Insufficient permissions to delete wiki")
            
        # Delete all related data
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            
            # Get all pages in wiki
            cursor.execute("SELECT id FROM pages WHERE wiki_id = ?", (wiki_id,))
            page_ids = [row[0] for row in cursor.fetchall()]
            
            # Delete page history
            for page_id in page_ids:
                cursor.execute("DELETE FROM page_history WHERE page_id = ?", (page_id,))
            
            # Delete pages
            cursor.execute("DELETE FROM pages WHERE wiki_id = ?", (wiki_id,))
            
            # Delete media
            cursor.execute("DELETE FROM media WHERE wiki_id = ?", (wiki_id,))
            
            # Finally delete wiki
            cursor.execute("DELETE FROM wikis WHERE id = ?", (wiki_id,))
            conn.commit()
            
        return True

    def get_all_wiki_instances(self):
        return self.wiki_system.get_all_wiki_instances()

    ###########################################################################
    # Page Operations
    ###########################################################################
    def create_page(self, wiki_id, title, content, user, slug):
        import traceback
        try:
            """Create new page with debug logging"""
            print(f"DEBUG: create_page(wiki_id={wiki_id}, title='{title}', slug='{slug}')")
            import datetime
            created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
                query = """
                    INSERT INTO pages 
                    (title, content, wiki_id, created_by, slug, created_at, updated_at) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                params = (title, content, wiki_id, user.id, slug, created_at, created_at)
                print(f"DEBUG: SQL Query: {query}")
                print(f"DEBUG: Params: {params}")
                
                cursor.execute(query, params)
                page_id = cursor.lastrowid
                conn.commit()
                
                print(f"DEBUG: Page inserted - ID: {page_id}")
                
        except (WikiNotFound, UnauthorizedAccess) as e:
            print(f"DEBUG ERROR: {type(e).__name__}: {str(e)}")
            status = 404 if isinstance(e, WikiNotFound) else 403
            return print(f"{e} status")
        except HTTPResponse as e:
            # Allow redirects to propagate normally
            raise e
        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")
            traceback.print_exc()
            return print(f"Error creating page: {str(e)}")  


        return WikiPage(
                id=page_id,
                title=title,
                content=content,
                wiki_id=wiki_id,
                created_by=user.id,
                created_at=created_at,
                updated_at=created_at,
                slug=slug
            )        
    
    def get_page_by_slug(self, wiki_id, page_slug):
        """Get page by slug - DEBUGGED VERSION"""
        print(f"DEBUG: get_page_by_slug(wiki_id={wiki_id}, page_slug='{page_slug}')")
        
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = "SELECT * FROM pages WHERE wiki_id = ? AND slug = ?"
            print(f"DEBUG: SQL Query: {query} with params ({wiki_id}, '{page_slug}')")
            
            cursor.execute(query, (wiki_id, page_slug))
            row = cursor.fetchone()
            
            if row:
                print(f"DEBUG: Found page: ID={row['id']}")
                return WikiPage(
                    id=row['id'],
                    title=row['title'],
                    content=row['content'],
                    wiki_id=row['wiki_id'],
                    created_by=row['created_by'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    slug=row['slug']
                )
            else:
                print(f"DEBUG: Page not found: wiki_id={wiki_id}, slug='{page_slug}'")
                return None

    def page_slug_exists(self, wiki_id, slug):
        """Check if slug exists with debug logging"""
        print(f"DEBUG: page_slug_exists(wiki_id={wiki_id}, slug='{slug}')")
        
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM pages WHERE wiki_id = ? AND slug = ?"
            print(f"DEBUG: SQL Query: {query} with params ({wiki_id}, '{slug}')")
            
            cursor.execute(query, (wiki_id, slug))
            count = cursor.fetchone()[0]
            exists = count > 0
            
            print(f"DEBUG: Slug exists? {exists}")
            return exists

    def update_page(self, page, editor, comment="Updated"):
        """Update page content with history tracking and permission check"""
        if not isinstance(editor, AuthUser):
            editor = self.user_service.get_user_by_id(editor)
            
        if not PermissionSystem.can(editor, PermissionSystem.EDIT_PAGE, page.wiki_id):
            raise UnauthorizedAccess("Insufficient permissions to edit page")
        
        from datetime import datetime
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            # Update page
            cursor.execute(
                """UPDATE pages SET 
                title = ?, content = ?, updated_at = ?
                WHERE id = ?""",
                (page.title, page.content, updated_at, page.id)
            )
            # Add to page history - FIXED: Added title field
            cursor.execute(
                """INSERT INTO page_history 
                (page_id, title, content, updated_by, updated_at, comment) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (page.id, page.title, page.content, editor.id, updated_at, comment)
            )
            conn.commit()
            
        return self.get_page_by_id(page.id)
    
    from collections import namedtuple
    
    class HistoryRecord:
        def __init__(self, id, title, content, updated_at, username, comment):
            self.id = id
            self.title = title
            self.content = content
            self.updated_at = updated_at
            self.username = username
            self.comment = comment

    def delete_page(self, page_id, deleter):
        """Delete a page with permission check"""
        page = self.get_page_by_id(page_id)
        
        if not isinstance(deleter, AuthUser):
            deleter = self.user_service.get_user_by_id(deleter)
            
        if not PermissionSystem.can(deleter, PermissionSystem.DELETE_PAGE, page.wiki_id):
            raise UnauthorizedAccess("Insufficient permissions to delete page")

        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM page_media WHERE page_id = ?", (page_id,))
            cursor.execute("DELETE FROM page_history WHERE page_id = ?", (page_id,))
            cursor.execute("DELETE FROM pages WHERE id = ?", (page_id,))
            conn.commit()
            
        return True

    def get_page_history(self, page_id):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT ph.id, ph.title, ph.content, ph.updated_at, u.username, ph.comment 
                FROM page_history ph
                JOIN users u ON ph.updated_by = u.id
                WHERE page_id = ?
                ORDER BY ph.updated_at DESC""",
                (page_id,)
            )
            return [
                {
                    "id": row[0],
                    "title": row[1],  # Added title field
                    "content": row[2],
                    "updated_at": row[3],
                    "username": row[4],
                    "comment": row[5]
                }
                for row in cursor.fetchall()
            ]

    def get_wiki_pages(self, wiki_id):
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row  # Enable row factory
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM pages WHERE wiki_id = ? ORDER BY created_at DESC",
                (wiki_id,)
            )
            return [
                WikiPage(
                    id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    wiki_id=row["wiki_id"],
                    created_by=row["created_by"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                    slug=row["slug"]
                )
                for row in cursor.fetchall()
            ]

    ###########################################################################
    # Media Operations
    ###########################################################################
    def upload_media(self, file_upload, wiki_id, uploaded_by):
        """Handle media upload for a wiki with permission check"""
        if not isinstance(uploaded_by, AuthUser):
            uploaded_by = self.user_service.get_user_by_id(uploaded_by)
            

        if not PermissionSystem.can(uploaded_by, PermissionSystem.EDIT_PAGE, wiki_id):
            raise UnauthorizedAccess("Insufficient permissions to upload media")


        if not file_upload or not file_upload.filename:
            raise ValueError("No file uploaded")
            
        # valida o tipo de arq
        ext = os.path.splitext(file_upload.filename)[1].lower()
        allowed_types = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf")
        if ext not in allowed_types:
            raise InvalidMediaType(f"Invalid file type. Allowed: {', '.join(allowed_types)}")


        upload_path = get_wiki_upload_path()
        uuid_name = f"{uuid.uuid4().hex}{ext}"
        file_path = f"wiki/{wiki_id}/{uuid_name}"
        full_path = os.path.join(upload_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)


        file_upload.save(full_path, overwrite=True)
        file_size = os.path.getsize(full_path)


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
                    file_path,
                ),
            )
            media_id = cursor.lastrowid
            conn.commit()

        return self.get_media_by_id(media_id)

    def get_page_media(self, page_id):
        """pega a media acossiada com a pagina, a media é guardada separadamente da pagina, pode ser reutilizado por outros"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT m.id, m.uuid_filename, m.original_filename, 
                m.mime_type, m.file_size, m.wiki_id, m.uploaded_by, 
                m.uploaded_at, m.file_path 
                FROM media m
                JOIN page_media pm ON pm.media_id = m.id
                WHERE pm.page_id = ?""",
                (page_id,)
            )
            return [
                MediaItem(
                    id=row[0],
                    uuid_filename=row[1],
                    original_filename=row[2],
                    mime_type=row[3],
                    file_size=row[4],
                    wiki_id=row[5],
                    uploaded_by=row[6],
                    uploaded_at=row[7],
                    file_path=row[8]
                )
                for row in cursor.fetchall()
            ]

    ###########################################################################
    # Content Rendering
    ###########################################################################
    def render_markdown(self, markdown_content):
        """Convert Markdown to HTML with proper extensions"""
        if not markdown_content:
            return ""
        
        try:
            return markdown(
                markdown_content,
                extensions=[
                    'fenced_code',
                    'codehilite',
                    'tables',
                    'toc'
                ],
                output_format='html5'
            )
        except Exception as e:
            print(f"Markdown rendering error: {str(e)}")
            return f"<pre>{markdown_content}</pre>"

    ###########################################################################
    # User Contributions & Dashboard
    ###########################################################################
    def get_user_contributions(self, user_id):
        """Get comprehensive user contributions"""
        contributions = {
            "wikis_created": [],
            "pages_created": [],
            "edits": []
        }
        
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            
            # kis creaated
            cursor.execute(
                "SELECT id, name, slug FROM wikis WHERE owner_id = ?",
                (user_id,)
            )
            contributions["wikis_created"] = [
                {"id": row[0], "name": row[1], "slug": row[2]}
                for row in cursor.fetchall()
            ]
            
            # PAges create
            cursor.execute(
                "SELECT id, title, slug FROM pages WHERE created_by = ?",
                (user_id,)
            )
            contributions["pages_created"] = [
                {"id": row[0], "title": row[1], "slug": row[2]}
                for row in cursor.fetchall()
            ]
            
            # edits
            cursor.execute(
                """SELECT ph.id, p.title, w.slug, ph.updated_at 
                FROM page_history ph
                JOIN pages p ON ph.page_id = p.id
                JOIN wikis w ON p.wiki_id = w.id
                WHERE ph.updated_by = ?
                ORDER BY ph.updated_at DESC
                LIMIT 50""",
                (user_id,)
            )
            contributions["edits"] = [
                {
                    "id": row[0],
                    "page_title": row[1],
                    "wiki_slug": row[2],
                    "timestamp": row[3]
                }
                for row in cursor.fetchall()
            ]
            
        return contributions

    def get_user_dashboard_data(self, user_id):
        """Get comprehensive data for user dashboard"""
        dashboard_data = {
            "owned_wikis": [],
            "moderated_wikis": [],
            "recent_edits": [],
            "created_pages": []
        }
        
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # wikis owned by user
            cursor.execute("""
                SELECT id, name, slug, created_at 
                FROM wikis 
                WHERE owner_id = ?
                ORDER BY created_at DESC
                LIMIT 10
            """, (user_id,))
            dashboard_data["owned_wikis"] = [dict(row) for row in cursor.fetchall()]
            
            # wikis that user moderates
            cursor.execute("""
                SELECT w.id, w.name, w.slug, w.created_at
                FROM wikis w
                INNER JOIN users u ON json_extract(u.wiki_roles, '$."' || w.id || '"') IN ('moderator', 'admin')
                WHERE u.id = ? AND w.owner_id != ?
            """, (user_id, user_id))
            dashboard_data["moderated_wikis"] = [dict(row) for row in cursor.fetchall()]
            
            #edits rec
            cursor.execute("""
                SELECT ph.id, p.title, w.slug AS wiki_slug, p.slug AS page_slug, 
                       ph.updated_at, u.username AS editor
                FROM page_history ph
                JOIN pages p ON ph.page_id = p.id
                JOIN wikis w ON p.wiki_id = w.id
                JOIN users u ON ph.updated_by = u.id
                WHERE ph.updated_by = ?
                ORDER BY ph.updated_at DESC
                LIMIT 15
            """, (user_id,))
            dashboard_data["recent_edits"] = [dict(row) for row in cursor.fetchall()]
            
            # pg made by user
            cursor.execute("""
                SELECT p.id, p.title, p.slug, w.slug AS wiki_slug, p.created_at
                FROM pages p
                JOIN wikis w ON p.wiki_id = w.id
                WHERE p.created_by = ?
                ORDER BY p.created_at DESC
                LIMIT 10
            """, (user_id,))
            dashboard_data["created_pages"] = [dict(row) for row in cursor.fetchall()]
        
        return dashboard_data

    ###########################################################################
    # Category Operations
    ###########################################################################
    def get_all_categories(self):
        """Get all categories without wikis"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def get_category(self, category_id):
        """Get single category by ID"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(row)

    def get_all_categories_with_wikis(self):
        """Get all categories with their associated wikis"""
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get categories with their wikis
            cursor.execute("""
    SELECT c.id AS category_id, c.name AS category_name, c.slug AS category_slug,
           c.color, c.icon,
           w.id AS wiki_id, w.name AS wiki_name, w.slug AS wiki_slug, 
           w.owner_id, w.created_at, u.username AS owner_username
    FROM categories c
    LEFT JOIN wikis w ON c.id = w.category_id
    LEFT JOIN users u ON w.owner_id = u.id
    ORDER BY c.name, w.name
""")        
            categories = {}
            for row in cursor.fetchall():
                cat_id = row["category_id"]
                if cat_id not in categories:
                    categories[cat_id] = {
                        'id': cat_id,
                        'name': row["category_name"],
                        'slug': row["category_slug"],
                        'color': row["color"],
                        'icon': row["icon"],
                        'wikis': []
                    }
                
                if row["wiki_id"]:  # Some categories might be empty
                    wiki = {
                        'id': row["wiki_id"],
                        'name': row["wiki_name"],
                        'slug': row["wiki_slug"],
                        'owner_id': row["owner_id"],
                        'created_at': row["created_at"],
                        'owner_username': row["owner_username"]
                    }
                    categories[cat_id]['wikis'].append(wiki)
            
            # Also get uncategorized wikis
            cursor.execute("""
                SELECT w.id, w.name, w.slug, w.owner_id, w.created_at, u.username
                FROM wikis w
                JOIN users u ON w.owner_id = u.id
                WHERE w.category_id IS NULL
            """)
            uncategorized = [{
                'id': row["id"],
                'name': row["name"],
                'slug': row["slug"],
                'owner_id': row["owner_id"],
                'created_at': row["created_at"],
                'owner_username': row["username"]
            } for row in cursor.fetchall()]
            
            # Add uncategorized as a special category
            if uncategorized:
                categories[0] = {
                    'id': 0,
                    'name': 'Uncategorized',
                    'slug': 'uncategorized',
                    'color': '#6b7280',
                    'icon': 'folder-open',
                    'wikis': uncategorized
                }
            
            return list(categories.values())

    ###########################################################################
    # Helper & Debugging Methods
    ###########################################################################
    def get_wiki_by_id(self, wiki_id):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT w.*, u.username 
                FROM wikis w
                JOIN users u ON w.owner_id = u.id
                WHERE w.id = ?
            """, (wiki_id,))
            row = cursor.fetchone()
            if not row:
                raise WikiNotFound(f"Wiki with ID {wiki_id} not found")
            return WikiInstance(
                id=row[0],
                name=row[1],
                slug=row[2],
                owner_id=row[3],
                owner_username=row[5],
                created_at=row[4]
            )

    def get_page_by_id(self, page_id):
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row  # Add this
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pages WHERE id = ?", (page_id,))
            row = cursor.fetchone()
            if not row:
                raise PageNotFound(f"Page with ID {page_id} not found")
                
            return WikiPage(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                wiki_id=row["wiki_id"],
                created_by=row["created_by"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                slug=row["slug"] 
            )

    def get_wiki_page_count(self, wiki_id):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pages WHERE wiki_id = ?", (wiki_id,))
            return cursor.fetchone()[0]
    
    
    def get_wiki_admins(self, wiki_id):
        """Get admin users for a wiki"""
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username 
                FROM users
                WHERE json_extract(wiki_roles, '$."' || ? || '"') = ?
            """, (str(wiki_id), "admin"))
        return [dict(row) for row in cursor.fetchall()] 





