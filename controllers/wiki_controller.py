import os
import re
import time
import traceback
from contextlib import closing

from bottle import (TEMPLATE_PATH, Bottle, HTTPResponse, SimpleTemplate,
                    redirect, request, response, static_file, template)

from config import SECRET_KEY, TEMPLATE_DIR
from data import get_db_connection, get_wiki_upload_path
from models.permSystem import PermissionSystem
from models.user import AuthUser
from models.wiki import MediaItem, WikiInstance, WikiPage, WikiSystem
from services import user_service
from services.user_service import UserService
from services.wiki_service import WikiService


# tratamento de erro, ainda nao implementado, talvez n de tempo
class WikiNotFound(Exception): pass
class PageNotFound(Exception): pass
class UnauthorizedAccess(Exception): pass
class MediaNotFound(Exception): pass
class InvalidMediaType(Exception): pass

wiki_routes = Bottle()
TEMPLATE_PATH.insert(0, TEMPLATE_DIR)

class WikiController:
    def __init__(self, app):
        self.app = app
        self.user_service = UserService
        self.wiki_service = WikiService(self.user_service)
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/wikis", method="GET", callback=self.list_wikis)
        self.app.route("/wikis/create", method=["GET", "POST"], callback=self.create_wiki)
        self.app.route("/wikis/<wiki_slug>", method="GET", callback=self.view_wiki)
        self.app.route("/wikis/<wiki_slug>/edit", method=["GET", "POST"], callback=self.edit_wiki)
        self.app.route("/wikis/<wiki_slug>/delete", method="POST", callback=self.delete_wiki)
        
        # Page routes
        self.app.route("/wikis/<wiki_slug>/pages/create", method=["GET", "POST"], callback=self.create_page)
        self.app.route("/wikis/<wiki_slug>/<page_slug>", method="GET", callback=self.view_page)
        self.app.route("/wikis/<wiki_slug>/<page_slug>/edit", method=["GET", "POST"], callback=self.edit_page)
        self.app.route("/wikis/<wiki_slug>/<page_slug>/delete", method="POST", callback=self.delete_page)
        self.app.route("/wikis/<wiki_slug>/<page_slug>/history", method="GET", callback=self.page_history)
        self.app.route("/wikis/create/form", method="GET", callback=self.get_create_wiki_form)
        self.app.route("/wikis/<wiki_slug>/pages/create", method=["GET", "POST"], callback=self.create_page)
        self.app.route("/wikis/<wiki_slug>/<page_slug>", method="GET", callback=self.view_page)
        # Media routes
        self.app.route("/wikis/<wiki_slug>/upload-media", method="POST", callback=self.upload_media)
        self.app.route("/media/<wiki_id:int>/<filename>", method="GET", callback=self.serve_media)
        self.app.route("/media/delete/<media_id:int>", method="POST", callback=self.delete_media)
        # dev routes
        self.app.route("/dev/wiki-debug", method="GET", callback=self.dev_wiki_debug)

    def get_current_user(self):
        """Get authenticated user from session"""
        user_id = request.get_cookie("user_id", secret=SECRET_KEY)
        if user_id:
            return self.user_service.get_user_by_id(int(user_id))
        return None

    def render_template(self, template_name, **kwargs):
        """Render template with common context"""
        from config import TEMPLATE_DIR
        template_path = os.path.join(TEMPLATE_DIR, template_name)
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        user = self.get_current_user()
        base_context = {
            "user": user,
            "PermissionSystem": PermissionSystem,
            "request": request
        }
        context = {**base_context, **kwargs}
        
        tpl = SimpleTemplate(template_content)
        return template(template_name, template_lookup=[TEMPLATE_DIR], **context)
    
    def render_error(self, message, status=500):
        """Render error page"""
        response.status = status
        return self.render_template(
            "error.tpl",
            error_message=message,
            status_code=status
        )

    def list_wikis(self):
        try:
            print("searching wiki!!!")
            wikis = self.wiki_service.get_all_categories_with_wikis()
            categories = self.wiki_service.get_all_categories_with_wikis()
            user = self.get_current_user()
            return self.render_template(
                "wiki_view.tpl",
                categories = categories,
                wikis=wikis,
                user = user,
                PermissionSystem = PermissionSystem,
                error = None
            )
        except Exception as e:
            import traceback
            print(f"Error loading wikis: {str(e)}")
            traceback.print_exc()
            return self.render_error(f"Error loading wikis: {str(e)}")

    def create_wiki(self):
     user = self.get_current_user()
     if not user:
         return redirect("/login")
    
    # Determine if this is an HTMX request
     if not PermissionSystem.can(user, PermissionSystem.CREATE_WIKI):
         return self.render_error("you dont have permission to create a wiki!")
     hx_mode = request.headers.get('HX-Request') == 'true'
    
    # Fetch categories (moved to top level)
     with closing(get_db_connection()) as conn:
         cursor = conn.cursor()
         cursor.execute("SELECT id, name FROM categories ORDER BY name")
         categories = [dict(id=row[0], name=row[1]) for row in cursor.fetchall()]

     if request.method == "GET":
         return self.render_template(
             "wiki_form.tpl", 
             categories=categories,
             wiki=None,
            action_url="/wikis/create", 
            cancel_url="/wikis",
            hx_mode=hx_mode
        )
    
    # Process form data
     name = request.forms.get("name", "").strip()
     slug = request.forms.get("slug", "").strip()
     description = request.forms.get("description", "").strip()
     category_id = request.forms.get("category_id","").strip()
     category_id = int(category_id) if category_id else None
    
     errors = []
     if not name:
         errors.append("Wiki name is required")
     if not slug:
         if name:
             slug = re.sub(r'[^a-z0-9-]+', '', name.lower().replace(' ', '-'))
             slug = re.sub(r'-+$', '', slug)
         else:
             errors.append("Name is required to generate a slug")

     if slug and not re.match(r'^[a-z0-9\-]+$', slug):
         errors.append("Slug can only contain lowercase letters, numbers, and hyphens")
    
     if errors:
         return self.render_template(
            "wiki_form.tpl",
            wiki=None,
            categories=categories,  # Added categories here
            errors=errors,
            action_url="/wikis/create",
            cancel_url="/wikis",
            hx_mode=hx_mode
        )
    
     try:
         wiki = self.wiki_service.create_wiki(name, slug, description, user,category_id)
         if hx_mode:
             response.headers['HX-Trigger'] = 'newWikiCreated'
             return '''
            <div class="text-center p-4">
                <i class="fas fa-check-circle text-green-500 text-4xl mb-3"></i>
                <h3 class="text-xl font-bold mb-2">Wiki Created!</h3>
                <p>Your wiki has been created successfully.</p>
                <div class="mt-4">
                    <a href="/wikis/{}" class="btn btn-primary mr-2">
                        View Wiki
                    </a>
                    <button class="btn" 
                        _="on click remove .show from #create-wiki-modal then wait 200ms then set #create-wiki-modal's innerHTML to ''">
                        Close
                    </button>
                </div>
            </div>
            '''.format(slug)
        
         return redirect(f"/wikis/{wiki.slug}")
     except Exception as e:
         errors = [f"Error creating wiki: {str(e)}"]
         return self.render_template(
            "wiki_form.tpl",
            wiki=None,
            categories=categories,  # Added categories here
            errors=errors,
            action_url="/wikis/create", 
            cancel_url="/wikis",
            hx_mode=hx_mode  
        )     
    def get_create_wiki_form(self):
        """Return just the form for creating a wiki (for HTMX)"""
        user = self.get_current_user()
        if not user:
            return HTTPResponse(status=401, body="Unauthorized")
        return self.render_template(
            "wiki_form.tpl", 
            wiki=None,
            action_url="/wikis/create", 
            cancel_url="#",
            hx_mode=True
        )

    def view_wiki(self, wiki_slug):
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            pages = self.wiki_service.get_wiki_pages(wiki.id)
            
            # get desc wiki
            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT description FROM wikis WHERE id = ?", 
                    (wiki.id,)
                )
                result = cursor.fetchone()
                wiki.description = result[0] if result else ""
            
            return self.render_template(
                "wiki_single.tpl",
                wiki=wiki,
                pages=pages
            )
        except WikiNotFound:
            return self.render_error("Wiki not found", 404)
        except Exception as e:
            return self.render_error(f"Error loading wiki: {str(e)}")

    def edit_wiki(self, wiki_slug):
        user = self.get_current_user()
        if not user:
            return redirect("/login")
            
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            
            # checa permissoes
            print("trying to get permission to edit wiki:")
            if not PermissionSystem.can(user, PermissionSystem.MANAGE_WIKI, wiki.id):
                return self.render_error("You don't have permission to edit this wiki", 403)
                
            if request.method == "GET":
                # Get current description
                with closing(get_db_connection()) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT description FROM wikis WHERE id = ?", 
                        (wiki.id,)
                    )
                    result = cursor.fetchone()
                    wiki.description = result[0] if result else ""
                    
                return self.render_template(
                    "wiki_form.tpl",
                    wiki=wiki,
                    action_url=f"/wikis/{wiki_slug}/edit",  
                    cancel_url=f"/wikis/{wiki_slug}"
                )
                
            # Process form data
            name = request.forms.get("name", "").strip()
            slug = request.forms.get("slug", "").strip()
            description = request.forms.get("description", "").strip()
            category_id = request.forms.get("category_id", "").strip()
            category_id = int(category_id) if category_id else None
            print(f"form data: name:{name},slug:{slug}, desc:{description}")
            
            errors = []
            if not name:
                errors.append("Wiki name is required")
            if not slug:
                errors.append("URL slug is required")
            if not re.match(r'^[a-z0-9\-]+$', slug):
                errors.append("Slug can only contain lowercase letters, numbers, and hyphens")
            
            if errors:
                return self.render_template(
                    "wiki_form.tpl",
                    wiki=wiki,
                    errors=errors,
                    action_url=f"/wikis/{wiki_slug}/edit",  
                    cancel_url=f"/wikis/{wiki_slug}"
                )

            # Update wiki
            wiki.name = name
            wiki.slug = slug
            self.wiki_service.update_wiki(wiki,user)
            
            # Update description
            with closing(get_db_connection()) as conn:
             cursor = conn.cursor()
            cursor.execute(
            "UPDATE wikis SET category_id = ? WHERE id = ?",
            (category_id, wiki.id)
        )
            conn.commit()

            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE wikis SET description = ? WHERE id = ?",
                    (description, wiki.id)
                )
                conn.commit()
                
            return redirect(f"/wikis/{slug}")
            
        except WikiNotFound:
            return self.render_error("Wiki not found", 404)
        except UnauthorizedAccess as e:
            return self.render_error(str(e), 403)
        except Exception as e:
            return self.render_error(f"Error updating wiki: {str(e)}")

    def delete_wiki(self, wiki_slug):
        user = self.get_current_user()
        if not user:
            return redirect("/login")
            
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            self.wiki_service.delete_wiki(wiki.id, user)
            return redirect("/wikis")
            
        except WikiNotFound:
            return self.render_error("Wiki not found", 404)
        except UnauthorizedAccess as e:
            return self.render_error(str(e), 403)
        except Exception as e:
            return self.render_error(f"Error deleting wiki: {str(e)}")

    # ===== PAGE HANDLERS =====
    def create_page(self, wiki_slug):
        """Create new page with enhanced debugging"""
        print(f"\n===== DEBUG: CREATE_PAGE STARTED =====")
        print(f"Wiki Slug: {wiki_slug}")
        
        user = self.get_current_user()
        if not user:
            print("DEBUG: No user - redirecting to login")
            return redirect("/login")
        
        try:
            print(f"DEBUG: Fetching wiki: {wiki_slug}")
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            print(f"DEBUG: Found wiki: ID={wiki.id}, Name={wiki.name}")
            
            # Debug permissions
            can_create = PermissionSystem.can(user, PermissionSystem.CREATE_PAGE, wiki.id)
            print(f"DEBUG: User permissions - CREATE_PAGE: {can_create}")
            print(f"DEBUG: User global role: {user.global_role}")
            print(f"DEBUG: User wiki roles: {user.wiki_roles}")
            
            if not can_create:
                print("DEBUG: Permission denied - rendering error")
                return self.render_error("Permission denied!", 403)
            
            if request.method == "GET":
                print("DEBUG: GET request - rendering form")
                return self.render_template(
                    "page_form.tpl",
                    page=None,
                    wiki=wiki,
                    action_url=f"/wikis/{wiki_slug}/pages/create",
                    cancel_url=f"/wikis/{wiki_slug}"
                )
            
            # Process form data
            title = request.forms.get("title", "").strip()
            raw_slug = request.forms.get("slug", "").strip()
            content = request.forms.get("content", "")
            print(f"DEBUG: Form data - Title: '{title}', Raw Slug: '{raw_slug}'")
            
            # Generate valid slug
            slug = self.generate_valid_slug(title, raw_slug)
            print(f"DEBUG: Generated slug: '{slug}'")
            
            errors = []
            if not title:
                errors.append("Title is required!")
            if not slug:
                errors.append("Could not generate valid slug from title")
            elif not re.match(r'^[a-z0-9\-]+$', slug):
                errors.append("Slug can only contain lowercase letters, numbers and hyphens")
            
            # Debug slug validation
            print(f"DEBUG: Slug validation errors: {errors}")
            
            # Check for existing page - DEBUGGED VERSION
            if slug and not errors:
                print(f"DEBUG: Checking slug existence: wiki_id={wiki.id}, slug={slug}")
                exists = self.wiki_service.page_slug_exists(wiki.id, slug)
                print(f"DEBUG: Slug exists? {exists}")
                if exists:
                    errors.append("A page with this slug already exists!")
            
            if errors:
                print(f"DEBUG: Validation errors found: {errors}")
                return self.render_template(
                    "page_form.tpl",
                    page=None,
                    wiki=wiki,
                    errors=errors,
                    action_url=f"/wikis/{wiki_slug}/pages/create",
                    cancel_url=f"/wikis/{wiki_slug}"
                )

            # Create the page
            print("DEBUG: Creating page...")
            page = self.wiki_service.create_page(wiki.id, title, content, user, slug)
            print(f"DEBUG: Page created - ID: {page.id}, Slug: {page.slug}")
            
            # Debug redirect
            redirect_url = f"/wikis/{wiki.slug}/{page.id}"
            print(f"DEBUG: Redirecting to: {redirect_url}")
            return redirect(redirect_url)
            
        except WikiNotFound as e:
            print(f"DEBUG ERROR: Wiki not found - {str(e)}")
            return self.render_error("Wiki not found", 404)
        except UnauthorizedAccess as e:
            print(f"DEBUG ERROR: Unauthorized - {str(e)}")
            return self.render_error(str(e), 403)
        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")
            traceback.print_exc()
            return self.render_error(f"Error creating page: {str(e)}")
    
    def generate_valid_slug(self, title, raw_slug):
        """Generate URL-safe slug with debug logging"""
        candidate = raw_slug or title
        print(f"DEBUG: Slug candidate: '{candidate}'")
        
        if not candidate:
            return ""
        
        # Step-by-step normalization with debug
        slug = candidate.lower()
        print(f"DEBUG: Step 1 - Lowercase: '{slug}'")
        
        slug = slug.replace(" ", "-").replace("_", "-")
        print(f"DEBUG: Step 2 - Replace spaces/underscores: '{slug}'")
        
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        print(f"DEBUG: Step 3 - Remove invalid chars: '{slug}'")
        
        slug = re.sub(r'-+', '-', slug)
        print(f"DEBUG: Step 4 - Consolidate hyphens: '{slug}'")
        
        slug = slug.strip("-")
        print(f"DEBUG: Step 5 - Trim hyphens: '{slug}'")
        
        return slug  

    def view_page(self, wiki_slug, page_slug):
        try:
            user = self.get_current_user()
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            page = self.wiki_service.get_page_by_slug(wiki.id, page_slug)
            
            if not page:
                raise PageNotFound(f"Page '{page_slug}' not found")
            
            # Render markdown content
            html_content = self.wiki_service.render_markdown(page.content)
            
            # Get page media
            media = self.wiki_service.get_page_media(page.id)
            
            # Get author information
            author = self.user_service.get_user_by_id(page.created_by)
            
            return self.render_template(
                "page_view.tpl",
                wiki=wiki,
                page=page,
                rendered_content=html_content,
                media=media,
                author_username=author.username if author else "Unknown",
                last_editor_username="",  # Implement if you have edit history
                can_edit=PermissionSystem.can(user, PermissionSystem.EDIT_PAGE, wiki.id) if user else False
            )
        except (WikiNotFound, PageNotFound) as e:
            return self.render_error(str(e), 404)
        except Exception as e:
            traceback.print_exc()
            return self.render_error(f"Error loading page: {str(e)}")
    def edit_page(self, wiki_slug, page_slug):
        user = self.get_current_user()
        if not user:
            return redirect("/login")
            
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            page = self.wiki_service.get_page_by_slug(wiki.id, page_slug)
            
            # Checa perms
            if not PermissionSystem.can(user, PermissionSystem.EDIT_PAGE, wiki.id):
                return self.render_error("Usuario não tem permissão para editar!", 403)
                
            if request.method == "GET":
                # pega media da sidebar
                media = self.wiki_service.get_page_media(page.id)
                
                return self.render_template(
                    "page_form.tpl",
                    page=page,
                    wiki=wiki,
                    media=media,
                    action_url=f"/wikis/{wiki_slug}/{page_slug}/edit",  
                    cancel_url=f"/wikis/{wiki_slug}/{page_slug}"
                )
                
            title = request.forms.get("title", "").strip()
            slug = request.forms.get("slug", "").strip()
            content = request.forms.get("content", "")
            comment = request.forms.get("comment", "Updated content")
            
            errors = []
            if not title:
                errors.append("Titulo é necessario!")
            if not slug:
                errors.append("URL da slug é necessario")
            if not re.match(r'^[a-z0-9\-]+$', slug):
                errors.append("Slugs podem apenas ter letras, numeros e hifens!")
            
            if errors:
                # pega media sidebar de novo
                media = self.wiki_service.get_page_media(page.id)
                
                return self.render_template(
                    "page_form.tpl",
                    page=page,
                    wiki=wiki,
                    media=media,
                    errors=errors,
                    action_url=f"/wikis/{wiki_slug}/{page_slug}/edit",  
                    cancel_url=f"/wikis/{wiki_slug}/{page_slug}"
                )

            # uptd page
            page.title = title
            page.content = content
            self.wiki_service.update_page(page, user, comment)
            
            # update slug se ela mudar
            if page.slug != slug:
                page.slug = slug
                with closing(get_db_connection()) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE pages SET slug = ? WHERE id = ?",
                        (slug, page.id)
                    )
                    conn.commit()
                    
            return redirect(f"/wikis/{wiki.slug}/{slug}")

        except (WikiNotFound, PageNotFound):
            return self.render_error("Page not found", 404)
        except UnauthorizedAccess as e:
            return self.render_error(str(e), 403)
        except Exception as e:
            return self.render_error(f"Error updating page: {str(e)}")

    def delete_page(self, wiki_slug, page_slug):
        user = self.get_current_user()
        if not user:
            return redirect("/login")
            
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            page = self.wiki_service.get_page_by_slug(wiki.id, page_slug)
            self.wiki_service.delete_page(page.id, user)
            return redirect(f"/wikis/{wiki.slug}")
            
        except (WikiNotFound, PageNotFound):
            return self.render_error("Page not found", 404)
        except UnauthorizedAccess as e:
            return self.render_error(str(e), 403)
        except Exception as e:
            return self.render_error(f"Error deleting page: {str(e)}")

    def page_history(self, wiki_slug, page_slug):
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            page = self.wiki_service.get_page_by_slug(wiki.id, page_slug)
            history = self.wiki_service.get_page_history(page.id)
            
            return self.render_template(
                "page_history.tpl",
                wiki=wiki,
                page=page,
                history=history
            )
        except (WikiNotFound, PageNotFound):
            return self.render_error("Page not found", 404)
        except Exception as e:
            return self.render_error(f"Error loading page history: {str(e)}")

    # ===== HANDLERS PARA MEDIA  =====
    def upload_media(self, wiki_slug):
        user = self.get_current_user()
        if not user:
            return HTTPResponse(status=401, body="Unauthorized")
            
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            # can eh o metodo pra checar permissoes para user
            if not PermissionSystem.can(user, PermissionSystem.EDIT_PAGE, wiki.id):
                return HTTPResponse(status=403, body="Forbidden")
                
            upload = request.files.get('media')
            if not upload:
                return HTTPResponse(status=400, body="No file uploaded")
                
            # Validate file size
            MAX_SIZE = 10 * 1024 * 1024  # 10MB
            upload.file.seek(0, 2)  
            file_size = upload.file.tell()
            upload.file.seek(0)
            
            if file_size > MAX_SIZE:
                return HTTPResponse(status=400, body="File size exceeds 10MB limit")
                
            # upload
            media_item = self.wiki_service.upload_media(
                upload, 
                wiki.id, 
                user.id
            )
            
            # Returna JSON com as infos da media
            response.content_type = 'application/json'
            return {
                "success": True,
                "filename": media_item.uuid_filename,
                "url": f"/media/{wiki.id}/{media_item.uuid_filename}",
                "id": media_item.id,
                "name": media_item.original_filename
            }
            
        except WikiNotFound:
            return HTTPResponse(status=404, body="Wiki not found")
        except InvalidMediaType as e:
            return HTTPResponse(status=400, body=str(e))
        except Exception as e:
            traceback.print_exc()
            return HTTPResponse(status=500, body=f"Server error: {str(e)}")

    def serve_media(self, wiki_id, filename):
        """Serve media files directly with caching"""
        try:
            # metadata da media 
            media = self.wiki_service.get_media_by_filename(wiki_id, filename)
            file_path = os.path.join(get_wiki_upload_path(), media.file_path)
            
            if not os.path.exists(file_path):
                raise MediaNotFound("File not found")
            
            response.set_header("Cache-Control", "public, max-age=31536000, immutable")
            
            return static_file(
                os.path.basename(file_path), 
                root=os.path.dirname(file_path))
        except MediaNotFound:
            return HTTPResponse(status=404, body="File not found")
        except Exception as e:
            return HTTPResponse(status=500, body=f"Error serving file: {str(e)}")

    def delete_media(self, media_id):
        user = self.get_current_user()
        if not user:
            return HTTPResponse(status=401, body="Unauthorized")
            
        try:
            media = self.wiki_service.get_media_by_id(media_id)
            
            if not PermissionSystem.can(user, PermissionSystem.MANAGE_WIKI, media.wiki_id):
                return HTTPResponse(status=403, body="Forbidden")
            
            file_path = os.path.join(get_wiki_upload_path(), media.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            # deleta da database
            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
                # deleta asociassoes
                cursor.execute(
                    "DELETE FROM page_media WHERE media_id = ?",
                    (media_id,)
                )
                # deleta da database
                cursor.execute(
                    "DELETE FROM media WHERE id = ?",
                    (media_id,)
                )
                conn.commit()
            
            return {"success": True}
        except MediaNotFound:
            return HTTPResponse(status=404, body="Media not found")
        except UnauthorizedAccess:
            return HTTPResponse(status=403, body="Permission denied")
        except Exception as e:
            traceback.print_exc()
            return HTTPResponse(status=500, body=f"Error deleting media: {str(e)}")

    # === INTEGRACAO COM A DASHBOARD
    def get_user_contributions(self, user_id):
        """Get user contributions for dashboard"""
        try:
            return self.wiki_service.get_user_contributions(user_id)
        except Exception as e:
            print(f"Error fetching user contributions: {str(e)}")
            return []

    # ==================================DEBUGGING THINGS
    def dev_wiki_debug(self):
        """Detailed debug route to test every step of wiki creation"""
        tests = []
        test_wiki = None
        
        # Test 1: Database connection
        try:
            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                tests.append({
                    "name": "Database Connection",
                    "status": "success",
                    "details": {
                        "action": "Connect to database and list tables",
                        "result": f"Found {len(tables)} tables",
                        "tables": ", ".join(tables)
                    }
                })
        except Exception as e:
            tests.append({
                "name": "Database Connection",
                "status": "error",
                "details": {
                    "action": "Connect to database",
                    "result": f"Failed: {str(e)}",
                    "solution": "Check database configuration and file permissions"
                }
            })
            return self.render_template("debug_report.tpl", tests=tests)  # Abort early

        # Test 2: User session
        try:
            user = self.get_current_user()
            if user:
                tests.append({
                    "name": "User Session",
                    "status": "success",
                    "details": {
                        "action": "Get current user from session",
                        "result": f"User found: {user.username} (ID: {user.id})",
                        "global_role": user.global_role,
                        "wiki_roles": f"{len(user.wiki_roles)} assigned roles"
                    }
                })
            else:
                tests.append({
                    "name": "User Session",
                    "status": "warning",
                    "details": {
                        "action": "Get current user from session",
                        "result": "No user logged in",
                        "solution": "Login required to test wiki creation"
                    }
                })
                return self.render_template("debug_report.tpl", tests=tests)  # Abort early
        except Exception as e:
            tests.append({
                "name": "User Session",
                "status": "error",
                "details": {
                    "action": "Get current user from session",
                    "result": f"Failed: {str(e)}",
                    "solution": "Check session configuration and user service"
                }
            })
            return self.render_template("debug_report.tpl", tests=tests)  # Abort early

        # Test 3: Permission system
        try:
            can_create = PermissionSystem.can(user, PermissionSystem.CREATE_WIKI)
            tests.append({
                "name": "Permission Check",
                "status": "success" if can_create else "error",
                "details": {
                    "action": "Check CREATE_WIKI permission",
                    "result": f"User has permission: {can_create}",
                    "required_permission": "CREATE_WIKI",
                    "user_permissions": str(user.permissions)
                }
            })
            if not can_create:
                return self.render_template("debug_report.tpl", tests=tests)  # Abort early
        except Exception as e:
            tests.append({
                "name": "Permission Check",
                "status": "error",
                "details": {
                    "action": "Check CREATE_WIKI permission",
                    "result": f"Failed: {str(e)}",
                    "solution": "Check permission system implementation"
                }
            })
            return self.render_template("debug_report.tpl", tests=tests)  # Abort early

        # Test 4: Wiki creation parameters
        try:
            test_slug = f"test-wiki-{int(time.time())}"
            test_name = "Test Wiki"
            test_desc = "Debug route test description"
            tests.append({
                "name": "Input Parameters",
                "status": "info",
                "details": {
                    "action": "Generate test parameters",
                    "name": test_name,
                    "slug": test_slug,
                    "description": test_desc
                }
            })
        except Exception as e:
            tests.append({
                "name": "Input Parameters",
                "status": "error",
                "details": {
                    "action": "Generate test parameters",
                    "result": f"Failed: {str(e)}",
                    "solution": "Check system time availability"
                }
            })
            return self.render_template("debug_report.tpl", tests=tests)  # Abort early

        # Test 5: Service layer - create_wiki
        try:
            wiki = self.wiki_service.create_wiki(test_name, test_slug, test_desc, user)
            test_wiki = wiki
            tests.append({
                "name": "Service Layer - Create Wiki",
                "status": "success",
                "details": {
                    "action": "Call wiki_service.create_wiki()",
                    "result": f"Wiki created successfully (ID: {wiki.id})",
                    "returned_object": f"WikiInstance(name='{wiki.name}', slug='{wiki.slug}')"
                }
            })
        except Exception as e:
            tests.append({
                "name": "Service Layer - Create Wiki",
                "status": "error",
                "details": {
                    "action": "Call wiki_service.create_wiki()",
                    "result": f"Failed: {str(e)}",
                    "solution": "Check WikiService implementation",
                    "traceback": traceback.format_exc()
                }
            })

        # Test 6: Database verification
        if test_wiki:
            try:
                with closing(get_db_connection()) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM wikis WHERE id = ?", (test_wiki.id,))
                    db_wiki = cursor.fetchone()
                    
                    if db_wiki:
                        tests.append({
                            "name": "Database Verification",
                            "status": "success",
                            "details": {
                                "action": "Verify wiki in database",
                                "result": "Wiki found in database",
                                "db_values": {
                                    "id": db_wiki[0],
                                    "name": db_wiki[1],
                                    "slug": db_wiki[2],
                                    "description": db_wiki[3] or "NULL",
                                    "owner_id": db_wiki[4],
                                    "created_at": db_wiki[5]
                                }
                            }
                        })
                    else:
                        tests.append({
                            "name": "Database Verification",
                            "status": "error",
                            "details": {
                                "action": "Verify wiki in database",
                                "result": "Wiki not found in database",
                                "solution": "Check database insert logic"
                            }
                        })
            except Exception as e:
                tests.append({
                    "name": "Database Verification",
                    "status": "error",
                    "details": {
                        "action": "Verify wiki in database",
                        "result": f"Failed: {str(e)}",
                        "solution": "Check database connection"
                    }
                })

        # Test 7: Load wiki by slug
        if test_wiki:
            try:
                loaded_wiki = self.wiki_service.get_wiki_by_slug(test_slug)
                tests.append({
                    "name": "Load Wiki by Slug",
                    "status": "success",
                    "details": {
                        "action": "Load wiki by slug from service",
                        "result": f"Successfully loaded wiki (ID: {loaded_wiki.id})",
                        "returned_object": f"WikiInstance(name='{loaded_wiki.name}', slug='{loaded_wiki.slug}')"
                    }
                })
            except Exception as e:
                tests.append({
                    "name": "Load Wiki by Slug",
                    "status": "error",
                    "details": {
                        "action": "Load wiki by slug from service",
                        "result": f"Failed: {str(e)}",
                        "solution": "Check get_wiki_by_slug implementation",
                        "traceback": traceback.format_exc()
                    }
                })

        # Test 8: Cleanup
        if test_wiki:
            try:
                with closing(get_db_connection()) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM wikis WHERE id = ?", (test_wiki.id,))
                    conn.commit()
                    tests.append({
                        "name": "Cleanup",
                        "status": "success",
                        "details": {
                            "action": "Delete test wiki from database",
                            "result": f"Deleted wiki ID: {test_wiki.id}",
                            "rows_affected": cursor.rowcount
                        }
                    })
            except Exception as e:
                tests.append({
                    "name": "Cleanup",
                    "status": "error",
                    "details": {
                        "action": "Delete test wiki from database",
                        "result": f"Failed: {str(e)}",
                        "solution": "Check database delete operations",
                        "traceback": traceback.format_exc()
                    }
                })

        return self.render_template("debug_report.tpl", tests=tests)

wiki_controller = WikiController(wiki_routes)
