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
