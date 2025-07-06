class Category:
    """Represents a category for organizing wikis"""

    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        description: str = "",
        color: str = "#6b7280",
        icon: str = "folder",
        wiki_count: int = 0,
    ):
        """
        Initialize a Category instance

        Args:
            id: Unique identifier for the category
            name: Display name of the category
            slug: URL-friendly identifier
            description: Optional description of the category
            color: Hex color code for display (default: neutral gray)
            icon: Font Awesome icon name (default: folder)
        """
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.color = color
        self.icon = icon
        self.wiki_count = wiki_count
        self._wikis = []  # Composition: Category owns its wiki references

    def add_wiki(self, wiki) -> None:
        """Add a wiki to this category"""
        if wiki not in self._wikis:
            self._wikis.append(wiki)
            wiki.category_id = self.id  # Maintain bidirectional reference

    def remove_wiki(self, wiki) -> bool:
        """Remove a wiki from this category"""
        if wiki in self._wikis:
            self._wikis.remove(wiki)
            wiki.category_id = None  # Remove reference
            return True
        return False

    def get_wikis(self) -> list:
        """Get all wikis in this category"""
        return self._wikis.copy()  # Return copy to prevent direct modification

    def __repr__(self) -> str:
        """Official string representation of the category"""
        return f"Category(id={self.id}, name='{self.name}', slug='{self.slug}')"

    def __str__(self) -> str:
        return f"{self.name} ({self.wiki_count} wikis)"
