import datetime
import json
from contextlib import closing

from data import get_db_connection

from models.user import AuthUser


class WikiSystem:
    """Representa o sistema wiki por inteiro, paginas e instancias"""

    def __init__(self):
        self._wiki_instances = (
            []
        )  # composicao, o sistema wiki e dono de TODAS as instancias

    def create_wiki_instance(self, name, slug, owner):
        """Create a new wiki instance (composition)"""
        instance = WikiInstance.create(name, slug, owner)
        self._wiki_instances.append(instance)
        return instance

    def _delete_wiki_instance(self, wiki_id):
        """Delete a wiki instance and all its content (composition)"""
        instance = self.get_wiki_instance(wiki_id)
        if instance:
            instance.delete() #deleta uma instancia inteira
            self._wiki_instances = [
                wi for wi in self._wiki_instances if wi.id != wiki_id
            ]
            return True
        return False

    def get_wiki_instance(self, wiki_id):
        if not self._wiki_instances:
            self._load_wiki_instances()
        return next((wi for wi in self._wiki_instances if wi.id == wiki_id), None)

    def get_all_wiki_instances(self):
        if not self._wiki_instances:
            self._load_wiki_instances()
        return self._wiki_instances

    def _load_wiki_instances(self):
        """carrega todas as instancias (privado)"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wikis")
            self._wiki_instances = [
                WikiInstance(
                    id=row["id"],
                    name=row["name"],
                    slug=row["slug"],
                    owner_id=row["owner_id"],
                    created_at=row["created_at"],
                )
                for row in cursor.fetchall()
            ]


class WikiInstance:
    """instancia de uma wiki n osistema"""

    def __init__(self, id, name, slug, owner_id, created_at):
        self.id = id
        self.name = name
        self.slug = slug
        self.owner_id = owner_id
        self.created_at = created_at
        self._pages = []  # composicao, instancia de wiki tem paginas
        self._moderators = []  # agregacao, moderadores sao usuarios referenciados

    def add_page(self, page):
        """Addiciona a pagina a essa instancia"""
        page.wiki_id = self.id
        self._pages.append(page)

    def get_pages(self):
        """pega todas as paginas de pela db"""
        if not self._pages:
            self._load_pages()
        return self._pages

    def delete_page(self, page_id):
        """Deleta a pagina pela db"""
        page = self.get_page(page_id)
        if page:
            page.delete()
            self._pages = [p for p in self._pages if p.id != page_id]
            return True
        return False

    def _load_pages(self):
        """carrega paginas pela db"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pages WHERE wiki_id = ?", (self.id,))
            self._pages = [
                WikiPage(
                    id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    wiki_id=row["wiki_id"],
                    created_by=row["created_by"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
                for row in cursor.fetchall()
            ]

    def add_moderator(self, user):
        """Agrega um usuario como moderador"""
        if user.id not in [m.id for m in self._moderators]:
            self._moderators.append(user)
            user.set_wiki_role(self.id, "moderator")

    def remove_moderator(self, user):
        """Remove o usuario e o degrada para viewer"""
        if user.id in [m.id for m in self._moderators]:
            self._moderators = [m for m in self._moderators if m.id != user.id]
            user.set_wiki_role(self.id, "view")  # downgrade pra viewer

    def get_moderators(self):
        """duh"""
        if not self._moderators:
            self._load_moderators()
        return self._moderators

    def _load_moderators(self):
        """pega mods pela db"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT u.* FROM users u
                WHERE json_extract(u.wiki_roles, '$."' || ? || '"') IN ('moderator', 'admin')
            """,
                (str(self.id),),
            )

            self._moderators = [
                AuthUser(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                    password_hash=row["password_hash"],
                    birthdate=row["birthdate"],
                    profile_picture=row["profile_picture"],
                    role=row["permissions"],
                    created_at=row["created_at"],
                    last_login=row["last_login"],
                    wiki_roles=json.loads(row["wiki_roles"]),
                )
                for row in cursor.fetchall()
            ]

    # Db Ops
    @classmethod
    def create(cls, name, slug, owner):
        """Cria uma instancia wiki"""
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO wikis (name, slug, owner_id, created_at) VALUES (?, ?, ?, ?)",
                (name, slug, owner.id, created_at),
            )
            wiki_id = cursor.lastrowid
            conn.commit()

        new_instance = cls(wiki_id, name, slug, owner.id, created_at)
        new_instance.add_moderator(owner)  # criador da wiki eh o moderador
        return new_instance

    def delete(self):
        """Deleta a wiki e todo seu conteudo"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            # deleta pages e media
            for page in self.get_pages():
                page.delete()
            # del  a wiki instancia inteira
            cursor.execute("DELETE FROM wikis WHERE id = ?", (self.id,))
            conn.commit()


class WikiPage:
    """Representa uma pagina em uma wiki instance"""

    def __init__(self, id, title, content, wiki_id, created_by, created_at, updated_at):
        self.id = id
        self.title = title
        self.content = content
        self.wiki_id = wiki_id
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at
        self._media = []  # agregacaoo, uma pagina tem midias
        self._author = None  # uma pagina tem um autor

    # Aggregation Relationships
    @property
    def author(self):
        """pega autor por id"""
        if not self._author:
            self._author = AuthUser.get_by_id(self.created_by)
        return self._author

    def add_media(self, media_item):
        """Associa a media com uma pagina"""
        if media_item.id not in [m.id for m in self._media]:
            self._media.append(media_item)
            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO page_media (page_id, media_id) VALUES (?, ?)",
                    (self.id, media_item.id),
                )
                conn.commit()

    def remove_media(self, media_id):
        """Remove a associacao de uma media com a pagina, nao deleta a media"""
        self._media = [m for m in self._media if m.id != media_id]
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM page_media WHERE page_id = ? AND media_id = ?",
                (self.id, media_id),
            )
            conn.commit()

    def get_media(self):
        """pega TODA a media para uma pagina"""
        if not self._media:
            self._load_media()
        return self._media

    def _load_media(self):
        """carrega img da db"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT m.* FROM media m
                JOIN page_media pm ON pm.media_id = m.id
                WHERE pm.page_id = ?
            """,
                (self.id,),
            )
            self._media = [
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

    # operacoes com db
    def save(self, user, comment="Updated"):
        """Salvar conteudo com o historico de editado"""
        edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        previous_content = self.content

        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            # Salvar o edit history
            cursor.execute(
                """INSERT INTO page_edit_history 
                (page_id, user_id, edit_time, edit_comment, content_before, content_after) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (self.id, user.id, edit_time, comment, previous_content, self.content),
            )
            # update
            cursor.execute(
                "UPDATE pages SET content = ?, updated_at = ? WHERE id = ?",
                (self.content, edit_time, self.id),
            )
            conn.commit()

    def delete(self):
        """Deleta a pagina e arruma a associacao de midias"""
        # deleta a pagina, mas nao a midia
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM page_media WHERE page_id = ?", (self.id,))
            cursor.execute("DELETE FROM pages WHERE id = ?", (self.id,))
            cursor.execute(
                "DELETE FROM page_edit_history WHERE page_id = ?", (self.id,)
            )
            conn.commit()


class MediaItem:
    """Representa a midia associada a uma wiki(gif,img etc)"""

    def __init__(
        self,
        id,
        uuid_filename,
        original_filename,
        mime_type,
        file_size,
        wiki_id,
        uploaded_by,
        uploaded_at,
        file_path,
    ):
        self.id = id
        self.uuid_filename = uuid_filename
        self.original_filename = original_filename
        self.mime_type = mime_type
        self.file_size = file_size
        self.wiki_id = wiki_id
        self.uploaded_by = uploaded_by
        self.uploaded_at = uploaded_at
        self.file_path = file_path

    def get_url(self):
        """url para mostrar a midia"""
        # NAO TEM ROTA PRONTA AINDA
        return f"/uploads/{self.file_path}"

    def delete_file(self):
        """Physically delete the media file from storage"""
        # escrever  a logica de deletar
        pass
