import os

from bottle import Bottle, redirect, request, response, static_file, template
from config import BASE_DIR, UPLOAD_DIR
from models import WikiInstance
from services.wiki_service import WikiService

# Create route container
wiki_routes = Bottle()

# Initialize service
wiki_service = WikiService()


class WikiController:
    def __init__(self, app):
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        # Wiki instance management
        @self.app.route("/wikis", method=["GET"])
        def list_wikis():
            wikis = wiki_service.get_all_wikis()
            return template("wiki/list_wikis", wikis=wikis)

        @self.app.route("/wikis/create", method=["GET", "POST"])
        def create_wiki():
            if request.method == "POST":
                title = request.forms.get("title")
                description = request.forms.get("description")
                category = request.forms.get("category")
                icon = request.files.get("icon")

                new_wiki = wiki_service.create_wiki(
                    title=title, description=description, category=category, icon=icon
                )
                redirect(f"/wikis/{new_wiki.id}")
            return template("wiki/create_wiki")

        @self.app.route("/wikis/<wiki_id>", method=["GET"])
        def view_wiki(wiki_id):
            wiki = wiki_service.get_wiki(wiki_id)
            recent_pages = wiki_service.get_recent_pages(wiki_id)
            return template("wiki/view_wiki", wiki=wiki, recent_pages=recent_pages)

        # Page management
        @self.app.route("/wikis/<wiki_id>/pages", method=["GET"])
        def list_pages(wiki_id):
            pages = wiki_service.get_all_pages(wiki_id)
            wiki = wiki_service.get_wiki(wiki_id)
            return template("page/list_pages", pages=pages, wiki=wiki)

        @self.app.route("/wikis/<wiki_id>/pages/create", method=["GET", "POST"])
        def create_page(wiki_id):
            wiki = wiki_service.get_wiki(wiki_id)

            if request.method == "POST":
                title = request.forms.get("title")
                content = request.forms.get("content")
                tags = request.forms.get("tags", "").split(",")

                new_page = wiki_service.create_page(
                    wiki_id=wiki_id, title=title, content=content, tags=tags
                )
                redirect(f"/wikis/{wiki_id}/pages/{new_page.id}")

            return template("page/create_page", wiki=wiki)

        @self.app.route("/wikis/<wiki_id>/pages/<page_id>", method=["GET"])
        def view_page(wiki_id, page_id):
            page = wiki_service.get_page(wiki_id, page_id)
            wiki = wiki_service.get_wiki(wiki_id)
            history = wiki_service.get_page_history(page_id)
            return template("page/view_page", page=page, wiki=wiki, history=history)

        @self.app.route("/wikis/<wiki_id>/pages/<page_id>/edit", method=["GET", "POST"])
        def edit_page(wiki_id, page_id):
            page = wiki_service.get_page(wiki_id, page_id)
            wiki = wiki_service.get_wiki(wiki_id)

            if request.method == "POST":
                title = request.forms.get("title")
                content = request.forms.get("content")
                tags = request.forms.get("tags", "").split(",")

                updated_page = wiki_service.update_page(
                    page_id=page_id, title=title, content=content, tags=tags
                )
                redirect(f"/wikis/{wiki_id}/pages/{page_id}")

            return template("page/edit_page", page=page, wiki=wiki)

        # Special routes
        @self.app.route("/wikis/<wiki_id>/search")
        def search_pages(wiki_id):
            query = request.query.get("q", "")
            results = wiki_service.search_pages(wiki_id, query)
            wiki = wiki_service.get_wiki(wiki_id)
            return template("search_results", results=results, wiki=wiki, query=query)

        @self.app.route("/wikis/<wiki_id>/uploads/<filename:path>")
        def serve_wiki_file(wiki_id, filename):
            return static_file(
                filename, root=os.path.join(UPLOAD_DIR, "wikis", wiki_id)
            )


# Initialize controller
WikiController(wiki_routes)
