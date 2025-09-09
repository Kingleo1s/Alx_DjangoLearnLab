from django.contrib import admin
from .models import Book

# Basic registration
# admin.site.register(Book)

# Customized admin class
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ("title", "author", "publication_year")

    # Add filters for quick filtering on the right side
    list_filter = ("publication_year", "author")

    # Add a search bar for these fields
    search_fields = ("title", "author")


