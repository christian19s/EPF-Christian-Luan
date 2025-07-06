from contextlib import closing

from data import get_db_connection
from models.category import Category


class CategoryService:
    def __init__(self):
        pass

    def create_category(
        self, name, slug, description="", color="#6b7280", icon="folder"
    ):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (name, slug, description, color, icon) VALUES (?, ?, ?, ?, ?)",
                (name, slug, description, color, icon),
            )
            category_id = cursor.lastrowid
            conn.commit()
        return self.get_category_by_id(category_id)

    def get_category_by_id(self, category_id):
        """Get a single category by ID as Category object"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
            row = cursor.fetchone()
            if row:
                return Category(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                    description=row[3],
                    color=row[4],
                    icon=row[5],
                )
        return None

    def get_all_categories(self):
        """Get all categories as list of Category objects"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
            SELECT c.*, COUNT(w.id) AS wiki_count 
            FROM categories c
            LEFT JOIN wikis w ON w.category_id = c.id
            GROUP BY c.id
            ORDER BY c.name
            """
            )
            rows = cursor.fetchall()

        return [
            Category(
                id=row[0],
                name=row[1],
                slug=row[2],
                description=row[3],
                color=row[4],
                icon=row[5],
                wiki_count=row[6],
            )
            for row in rows
        ]

    def update_category(self, category_id, name, slug, description, color, icon):
        """Update an existing category"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE categories SET name=?, slug=?, description=?, color=?, icon=? WHERE id=?",
                (name, slug, description, color, icon, category_id),
            )
            conn.commit()
        return self.get_category_by_id(category_id)

    def delete_category(self, category_id):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            try:
                # First remove category from all wikis
                cursor.execute(
                    "UPDATE wikis SET category_id = NULL WHERE category_id = ?",
                    (category_id,),
                )
                # Then delete the category
                cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                conn.rollback()
                raise e
