import os

from bottle import Bottle, HTTPResponse, request, static_file

from models.permSystem import PermissionSystem
from services import user_service
from services.media_service import MediaService
from services.user_service import UserService
from static.exceptions.exceptions import (
    InvalidMediaType,
    MediaNotFound,
    UnauthorizedAccess,
)

media_routes = Bottle()


class MediaController:
    def __init__(self, app, user_service):
        self.app = app
        self.user_service = user_service
        self.media_service = MediaService(user_service)
        self.setup_routes()

    def setup_routes(self):
        self.app.route(
            "/media/<wiki_id:int>/<filename>", method="GET", callback=self.serve_media
        )
        self.app.route(
            "/media/upload/<wiki_slug>", method="POST", callback=self.upload_media
        )
        self.app.route(
            "/media/delete/<media_id:int>", method="DELETE", callback=self.delete_media
        )

    def get_current_user(self, id):
        """Get authenticated user from session"""
        return UserService.get_user_by_id(id)

    def serve_media(self, wiki_id, filename):
        """Serve media files directly"""
        try:
            media = self.media_service.get_media_by_filename(wiki_id, filename)
            file_path = get_wiki_upload_path() / media.file_path

            if not os.path.exists(file_path):
                raise MediaNotFound("File not found")

            # cache na header
            response.set_header("Cache-Control", "public, max-age=31536000, immutable")

            return static_file(filename, root=str(file_path.parent))

        except MediaNotFound:
            return HTTPResponse(status=404, body="File not found")
        except Exception as e:
            return HTTPResponse(status=500, body=f"Error serving file: {str(e)}")

    def upload_media(self, wiki_slug):
        """Handle media uploads"""
        user = self.get_current_user(id)
        if not user:
            return HTTPResponse(status=401, body="Unauthorized")

        try:
            wiki = self.wiki_service.get_wiki_by_slug(wiki_slug)
            wiki_id = request.forms.get("wiki_id")
            if not wiki_id:
                return HTTPResponse(status=400, body="Missing wiki ID")

            # Check permissions
            if not PermissionSystem.can(user, PermissionSystem.EDIT_PAGE, int(wiki_id)):
                return HTTPResponse(status=403, body="Forbidden")

            upload = request.files.get("media")
            media_item = self.media_service.upload_media(upload, int(wiki_id), user)

            # Return JSON response
            return {
                "success": True,
                "media": {
                    "id": media_item.id,
                    "filename": media_item.uuid_filename,
                    "original": media_item.original_filename,
                    "url": f"/media/{wiki_id}/{media_item.uuid_filename}",
                    "type": media_item.mime_type,
                },
            }

        except InvalidMediaType as e:
            return HTTPResponse(status=400, body=str(e))
        except Exception as e:
            return HTTPResponse(status=500, body=f"Error uploading media: {str(e)}")

    def delete_media(self, media_id):
        """Delete media"""
        user = self.get_current_user()
        if not user:
            return HTTPResponse(status=401, body="Unauthorized")

        try:
            self.media_service.delete_media(media_id, user)
            return {"success": True}
        except (UnauthorizedAccess, MediaNotFound) as e:
            return HTTPResponse(status=404, body=str(e))
        except Exception as e:
            return HTTPResponse(status=500, body=f"Error deleting media: {str(e)}")


# Initialize controller
media_controller = MediaController(media_routes, UserService())
