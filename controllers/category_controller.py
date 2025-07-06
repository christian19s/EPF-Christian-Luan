import os
import sqlite3

from bottle import (Bottle, HTTPResponse, SimpleTemplate, redirect, request,
                    response, template)

from config import SECRET_KEY, TEMPLATE_DIR
from data import get_db_connection
from models.category import Category
from models.permSystem import PermissionSystem
from services.category_service import CategoryService
from services.user_service import UserService

category_routes = Bottle()


class CategoryController:
    def __init__(self, app):
        self.app = app
        self.user_service = UserService
        self.category_service = CategoryService()
        self.setup_routes()

    def setup_routes(self):
        self.app.route("/manage", method="GET", callback=self.manage_categories)
        self.app.route("/create", method=["GET", "POST"], callback=self.create_category)
        self.app.route(
            "/<category_id:int>/edit",
            method=["GET", "POST"],
            callback=self.edit_category,
        )
        self.app.route(
            "/<category_id:int>/delete", method="POST", callback=self.delete_category
        )

    def get_current_user(self):
        """Get authenticated user from session"""
        user_id = request.get_cookie("user_id", secret=SECRET_KEY)
        if user_id:
            return self.user_service.get_user_by_id(int(user_id))
        return None

    def render_template(self, template_name, **kwargs):
        """Render template with common context"""
        template_path = os.path.join(TEMPLATE_DIR, template_name)
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        user = self.get_current_user()
        base_context = {
            "user": user,
            "PermissionSystem": PermissionSystem,
            "request": request,
        }
        context = {**base_context, **kwargs}

        tpl = SimpleTemplate(template_content)
        return template(template_name, template_lookup=[TEMPLATE_DIR], **context)

    def render_error(self, message, status=500):
        """Render error page"""
        response.status = status
        return self.render_template(
            "error.tpl", error_message=message, status_code=status
        )

    def manage_categories(self):
        """Display all categories management page"""
        user = self.get_current_user()
        if not user:
            return redirect("/login")

        if not PermissionSystem.can(user, PermissionSystem.MANAGE_CATEGORIES):
            return self.render_error(
                "You don't have permission to manage categories", 403
            )

        try:
            categories = self.category_service.get_all_categories()
            return self.render_template("category_manage.tpl", categories=categories)
        except Exception as e:
            return self.render_error(f"Error loading categories: {str(e)}")

    def create_category(self):
     user = self.get_current_user()
     if not user:
         return redirect("/login")

     if not PermissionSystem.can(user, PermissionSystem.MANAGE_CATEGORIES):
         return self.render_error(
             "You don't have permission to create categories", 403
         )

     if request.method == "GET":
         return self.render_template("category_form.tpl", category=None)

    # Process POST data
     name = request.forms.get("name", "").strip()
     slug = request.forms.get("slug", "").strip()
     description = request.forms.get("description", "").strip()
     color = request.forms.get("color", "#6b7280").strip()
     icon = request.forms.get("icon", "folder").strip()

     errors = []
    # Basic validation
     if not name:
         errors.append("Category name is required")
     if not slug:
         errors.append("URL slug is required")
     elif len(slug) < 2:
         errors.append("Slug must be at least 2 characters long")

     if errors:
         form_data = {
            "name": name,
            "slug": slug,
            "description": description,
            "color": color,
            "icon": icon,
        }
         return self.render_template(
            "category_form.tpl", category=form_data, errors=errors
        )

     try:
         self.category_service.create_category(name, slug, description, color, icon)
         return redirect("/categories/manage")
     except sqlite3.IntegrityError as e:
         errors = []
         if "categories.slug" in str(e):
             errors.append("A category with this URL slug already exists")
         elif "categories.name" in str(e):
            errors.append("A category with this name already exists")
         else:
            errors.append("Database error: " + str(e))
        
         form_data = {
            "name": name,
            "slug": slug,
            "description": description,
            "color": color,
            "icon": icon,
        }
         return self.render_template(
            "category_form.tpl", category=form_data, errors=errors
        )
     except Exception as e:
         errors = [f"Error creating category: {str(e)}"]
         form_data = {
            "name": name,
            "slug": slug,
            "description": description,
            "color": color,
            "icon": icon,
        }
         return self.render_template(
            "category_form.tpl", category=form_data, errors=errors
        )
    def edit_category(self, category_id):
        """Handle category editing"""
        user = self.get_current_user()
        if not user:
            return redirect("/login")

        if not PermissionSystem.can(user, PermissionSystem.MANAGE_CATEGORIES):
            return self.render_error(
                "You don't have permission to edit categories", 403
            )

        try:
            category = self.category_service.get_category_by_id(category_id)
            if not category:
                return self.render_error("Category not found", 404)

            if request.method == "GET":
                return self.render_template("category_form.tpl", category=category)

            # Process POST data
            name = request.forms.get("name", "").strip()
            slug = request.forms.get("slug", "").strip()
            description = request.forms.get("description", "").strip()
            color = request.forms.get("color", "#6b7280").strip()
            icon = request.forms.get("icon", "folder").strip()

            errors = []
            if not name:
                errors.append("Category name is required")
            if not slug:
                errors.append("URL slug is required")

            if errors:
                 form_data = {
                 'id': category.id,
                 'name': category.name,
                  'slug': category.slug,
                 'description': category.description,
                 'color': category.color,
                 'icon': category.icon
                 }
                 return self.render_template("category_form.tpl", category=form_data)
            self.category_service.update_category(
                category_id, name, slug, description, color, icon
            )
            return redirect("/categories/manage")

        except Exception as e:
              return self.render_error(f"Error updating category: {str(e)}")

    def delete_category(self, category_id):
        """Handle category deletion"""
        user = self.get_current_user()
        if not user:
            return redirect("/login")

        if not PermissionSystem.can(user, PermissionSystem.MANAGE_CATEGORIES):
            return self.render_error(
                "You don't have permission to delete categories", 403
            )

        try:
            success = self.category_service.delete_category(category_id)
            if not success:
                return self.render_error("Category not found", 404)
            return redirect("/categories/manage")
        except Exception as e:
            return self.render_error(f"Error deleting category: {str(e)}")


category_controller = CategoryController(category_routes)
