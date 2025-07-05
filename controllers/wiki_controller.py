import os
import re
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


#tratamento de erro, ainda nao implementado, talvez n de tempo
class WikiNotFound(Exception): pass
class PageNotFound(Exception): pass
class UnauthorizedAccess(Exception): pass
class MediaNotFound(Exception): pass
class InvalidMediaType(Exception): pass
wiki_routes = Bottle()
TEMPLATE_PATH.insert(0,TEMPLATE_DIR)
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
        
        # Media routes
        self.app.route("/wikis/<wiki_slug>/upload-media", method="POST", callback=self.upload_media)
        self.app.route("/media/<wiki_id:int>/<filename>", method="GET", callback=self.serve_media)
        self.app.route("/media/delete/<media_id:int>", method="POST", callback=self.delete_media)

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
            wikis = self.wiki_service.get_all_wiki_instances()
            return self.render_template(
                "wiki_view.tpl",
                wikis=wikis
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

    
     if request.method == "GET":
         return self.render_template(
            "wiki_form.tpl", 
            wiki=None,
            action_url="/wikis/create", 
            cancel_url="/wikis",
            hx_mode=hx_mode
        ) # contexto hx e importante
    
    # Process form data
     name = request.forms.get("name", "").strip()
     slug = request.forms.get("slug", "").strip()
     description = request.forms.get("description", "").strip()
    
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
            wiki=None,
            errors=errors,
            action_url="/wikis/create",
            cancel_url="/wikis",
            hx_mode=hx_mode  # passa o modo para o tpl
        )
    
     try:
         wiki = self.wiki_service.create_wiki(name, slug, user)
         # add descricao pra wiki
         with closing(get_db_connection()) as conn:
             cursor = conn.cursor()
             cursor.execute(
                 "UPDATE wikis SET description = ? WHERE id = ?",
                 (description, wiki.id)
             )
             conn.commit()
        
        
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
        
         return redirect(f"/wikis/{slug}")
     except Exception as e:
         errors = [f"Error creating wiki: {str(e)}"]
         return self.render_template(
            "wiki_form.tpl",
            wiki=None,
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
                "wiki_view.tpl",
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
        user = self.get_current_user()
        if not user:
            return redirect("/login")
            
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            
            # Check permissions
            if not user.can(PermissionSystem.CREATE_PAGE, wiki.id):
                return self.render_error("You don't have permission to create pages", 403)
                
            if request.method == "GET":
                return self.render_template(
                    "page_form.tpl",
                    page=None,
                    wiki=wiki,
                    action_url=f"/wikis/{wiki_slug}/pages/create",  
                    cancel_url=f"/wikis/{wiki_slug}"
                )
                
            # form data process
            title = request.forms.get("title", "").strip()
            slug = request.forms.get("slug", "").strip()
            content = request.forms.get("content", "")
            
            errors = []
            if not title:
                errors.append("Page title is required")
            if not slug:
                errors.append("URL slug is required")
            if not re.match(r'^[a-z0-9\-]+$', slug):
                errors.append("Slug can only contain lowercase letters, numbers, and hyphens")
            
            if errors:
                return self.render_template(
                    "page_form.tpl",
                    page=None,
                    wiki=wiki,
                    errors=errors,
                    action_url=f"/wikis/{wiki_slug}/pages/create",  
                    cancel_url=f"/wikis/{wiki_slug}"
                )

            # Cria pagina
            page = self.wiki_service.create_page(wiki.id, title, content, user)
            
            # Salva slug pra db
            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE pages SET slug = ? WHERE id = ?",
                    (slug, page.id)
                )
                conn.commit()
                
            return redirect(f"/wikis/{wiki.slug}/{slug}")
            
        except WikiNotFound:
            return self.render_error("Wiki not found", 404)
        except UnauthorizedAccess as e:
            return self.render_error(str(e), 403)
        except Exception as e:
            return self.render_error(f"Error creating page: {str(e)}")

    def view_page(self, wiki_slug, page_slug):
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            page = self.wiki_service.get_page_by_slug(wiki.id, page_slug)
            
            # Render conteudo md da pag
            html_content = self.wiki_service.render_markdown(page.content)
            
            # pega media da pag
            media = self.wiki_service.get_page_media(page.id)
            
            return self.render_template(
                "page_view.tpl",
                wiki=wiki,
                page=page,
                rendered_content=html_content,
                media=media
            )
        except (WikiNotFound, PageNotFound):
            return self.render_error("Page not found", 404)
        except Exception as e:
            return self.render_error(f"Error loading page: {str(e)}")

    def edit_page(self, wiki_slug, page_slug):
        user = self.get_current_user()
        if not user:
            return redirect("/login")
            
        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            page = self.wiki_service.get_page_by_slug(wiki.id, page_slug)
            
            # Checa perms
            if not page.can_edit(user):
                return self.render_error("You don't have permission to edit this page", 403)
                
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
                errors.append("Page title is required")
            if not slug:
                errors.append("URL slug is required")
            if not re.match(r'^[a-z0-9\-]+$', slug):
                errors.append("Slug can only contain lowercase letters, numbers, and hyphens")
            
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
            #can eh o metodo pra checar permissoes para user
            if not user.can(PermissionSystem.EDIT_PAGE, wiki.id):
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
                
            #  upload
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
            
            if not user.can(PermissionSystem.MANAGE_WIKI, media.wiki_id):
                return HTTPResponse(status=403, body="Forbidden")
            
            file_path = os.path.join(get_wiki_upload_path(), media.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            #deleta da database
            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
               # deleta asociassoes
                cursor.execute(
                    "DELETE FROM page_media WHERE media_id = ?",
                    (media_id,)
                )
                #deleta da database
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



    #=== INTEGRACAO COM A DASHBOARD
    def get_user_contributions(self, user_id):
        """Get user contributions for dashboard"""
        try:
            return self.wiki_service.get_user_contributions(user_id)
        except Exception as e:
            print(f"Error fetching user contributions: {str(e)}")
            return []

wiki_controller = WikiController(wiki_routes)
