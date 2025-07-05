from bottle import route, view
from models.permSystem import PermissionSystem  # Import your permission system
from services.user_service import UserService
from services.wiki_service import WikiService


@route("/dev")
@view("dev_dashboard")
def dev_dashboard():
    # Initialize services
    user_service = UserService()
    wiki_service = WikiService(user_service)

    # Get all wikis with page counts and admins
    wikis = []
    for wiki in wiki_service.get_all_wiki_instances():
        wikis.append(
            {
                "id": wiki.id,
                "name": wiki.name,
                "slug": wiki.slug,
                "owner": wiki.owner_username,
                "page_count": wiki_service.get_wiki_page_count(wiki.id),
                "admins": wiki_service.get_wiki_admins(wiki.id),
            }
        )

    # Get all users
    users = user_service.get_all_users()

    return {"wikis": wikis, "users": users}
