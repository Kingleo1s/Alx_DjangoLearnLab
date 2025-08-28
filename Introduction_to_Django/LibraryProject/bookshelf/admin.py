# Register your models here.
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # fields to display in the list view
    list_display = ("title", "author", "publication_year")

    # fields you can filter by (sidebar filters)
    list_filter = ("publication_year", "author")

    # fields you can search in
    search_fields = ("title", "author")
