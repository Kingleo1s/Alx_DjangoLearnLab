from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ("title", "author", "publication_year")

    # Add filters for quick filtering on the right side
    list_filter = ("publication_year", "author")

    # Add a search bar for these fields
    search_fields = ("title", "author")




class CustomUserAdmin(UserAdmin):
    
    list_display = ("username", "email", "first_name", "last_name", "date_of_birth", "is_staff")

    
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )

    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)



