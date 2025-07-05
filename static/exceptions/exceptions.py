class UserNotFound(Exception):
    """Execssoes levantadas quando o usuario n é achado no sistema"""

    # pensa nisso como se fosse o trhow do java.
    def __init__(
        self, message="User not found", user_id=None, username=None, email=None
    ):
        self.message = message
        self.user_id = user_id
        self.username = username
        self.email = email
        super().__init__(message)

    def __str__(self):
        details = []
        if self.user_id:
            details.append(f"ID: {self.user_id}")
        if self.username:
            details.append(f"username: {self.username}")
        if self.email:
            details.append(f"email: {self.email}")

        if details:
            return f"{self.message} ({', '.join(details)})"
        return self.message


class UnauthorizedAccess(Exception):
    pass


class DuplicateUser(Exception):
    """Erro a ser levantado se o usuario ja ta cadastrado"""

    def __init__(self, message="User already exists", username=None, email=None):
        self.message = message
        self.username = username
        self.email = email
        super().__init__(message)

    def __str__(self):
        details = []
        if self.username:
            details.append(f"username: {self.username}")
        if self.email:
            details.append(f"email: {self.email}")

        if details:
            return f"{self.message} ({', '.join(details)})"
        return self.message


class AuthenticationFailed(Exception):
    """caso a autenticação falhe"""

    def __init__(self, message="Authentication failed", email=None):
        self.message = message
        self.email = email
        super().__init__(message)

    def __str__(self):
        if self.email:
            return f"{self.message} for email: {self.email}"
        return self.message


class PermissionDenied(Exception):
    """Caso o usuario nao tenha permissão"""

    # exemplo de uso: editor de wiki e guest
    def __init__(
        self, message="Permission denied", user_id=None, required_permission=None
    ):
        self.message = message
        self.user_id = user_id
        self.required_permission = required_permission
        super().__init__(message)

    def __str__(self):
        details = []
        if self.user_id:
            details.append(f"user ID: {self.user_id}")
        if self.required_permission:
            details.append(f"required: {self.required_permission}")

        if details:
            return f"{self.message} ({', '.join(details)})"
        return self.message


class InvalidInput(Exception):
    """Input de data invalido"""

    def __init__(self, message="Invalid input", field=None, value=None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)

    def __str__(self):
        if self.field:
            return f"{self.message} for field '{self.field}' with value '{self.value}'"
        return self.message


class TokenExpired(Exception):
    def __init__(self, message="Authentication token has expired"):
        self.message = message
        super().__init__(message)


class TokenInvalid(Exception):
    """token invalido"""

    def __init__(self, message="Invalid authentication token"):
        self.message = message
        super().__init__(message)


class WikiNotFound(Exception):
    """Exceção levantada quando uma wiki não é encontrada"""

    def __init__(self, message="Wiki not found", wiki_id=None, slug=None):
        self.message = message
        self.wiki_id = wiki_id
        self.slug = slug
        super().__init__(message)

    def __str__(self):
        details = []
        if self.wiki_id:
            details.append(f"ID: {self.wiki_id}")
        if self.slug:
            details.append(f"slug: {self.slug}")

        if details:
            return f"{self.message} ({', '.join(details)})"
        return self.message


class PageNotFound(Exception):
    """Exceção levantada quando uma página de wiki não é encontrada"""

    def __init__(self, message="Page not found", page_id=None, slug=None, wiki_id=None):
        self.message = message
        self.page_id = page_id
        self.slug = slug
        self.wiki_id = wiki_id
        super().__init__(message)

    def __str__(self):
        details = []
        if self.page_id:
            details.append(f"ID: {self.page_id}")
        if self.slug:
            details.append(f"slug: {self.slug}")
        if self.wiki_id:
            details.append(f"wiki ID: {self.wiki_id}")

        if details:
            return f"{self.message} ({', '.join(details)})"
        return self.message


class MediaNotFound(Exception):
    """Exceção levantada quando uma mídia não é encontrada"""

    def __init__(
        self, message="Media not found", media_id=None, filename=None, wiki_id=None
    ):
        self.message = message
        self.media_id = media_id
        self.filename = filename
        self.wiki_id = wiki_id
        super().__init__(message)

    def __str__(self):
        details = []
        if self.media_id:
            details.append(f"ID: {self.media_id}")
        if self.filename:
            details.append(f"filename: {self.filename}")
        if self.wiki_id:
            details.append(f"wiki ID: {self.wiki_id}")

        if details:
            return f"{self.message} ({', '.join(details)})"
        return self.message


class InvalidMediaType(Exception):
    """Exceção levantada quando um tipo de mídia inválido é fornecido"""

    def __init__(
        self,
        message="Invalid media type",
        filename=None,
        mime_type=None,
        allowed_types=None,
    ):
        self.message = message
        self.filename = filename
        self.mime_type = mime_type
        self.allowed_types = allowed_types or ["image/jpeg", "image/png", "image/gif"]
        super().__init__(message)

    def __str__(self):
        details = []
        if self.filename:
            details.append(f"file: {self.filename}")
        if self.mime_type:
            details.append(f"type: {self.mime_type}")

        details.append(f"allowed: {', '.join(self.allowed_types)}")

        return f"{self.message} ({'; '.join(details)})"


class WikiDatabaseError(Exception):
    """Exceção para erros gerais de banco de dados relacionados a wikis"""

    def __init__(
        self,
        message="Database operation failed",
        operation=None,
        entity=None,
        original_error=None,
    ):
        self.message = message
        self.operation = operation
        self.entity = entity
        self.original_error = str(original_error) if original_error else None
        super().__init__(message)

    def __str__(self):
        details = []
        if self.operation:
            details.append(f"operation: {self.operation}")
        if self.entity:
            details.append(f"entity: {self.entity}")
        if self.original_error:
            details.append(f"error: {self.original_error}")

        if details:
            return f"{self.message} ({'; '.join(details)})"
        return self.message


class WikiStorageError(Exception):
    """Exceção para problemas de armazenamento de arquivos de wiki"""

    def __init__(
        self,
        message="File storage operation failed",
        operation=None,
        path=None,
        original_error=None,
    ):
        self.message = message
        self.operation = operation
        self.path = path
        self.original_error = str(original_error) if original_error else None
        super().__init__(message)

    def __str__(self):
        details = []
        if self.operation:
            details.append(f"operation: {self.operation}")
        if self.path:
            details.append(f"path: {self.path}")
        if self.original_error:
            details.append(f"error: {self.original_error}")

        if details:
            return f"{self.message} ({'; '.join(details)})"
        return self.message


class WikiContentError(Exception):
    """Exceção para problemas de conteúdo de wiki"""

    def __init__(
        self,
        message="Wiki content error",
        content_type=None,
        page_id=None,
        original_error=None,
    ):
        self.message = message
        self.content_type = content_type
        self.page_id = page_id
        self.original_error = str(original_error) if original_error else None
        super().__init__(message)

    def __str__(self):
        details = []
        if self.content_type:
            details.append(f"type: {self.content_type}")
        if self.page_id:
            details.append(f"page ID: {self.page_id}")
        if self.original_error:
            details.append(f"error: {self.original_error}")

        if details:
            return f"{self.message} ({'; '.join(details)})"
        return self.message
