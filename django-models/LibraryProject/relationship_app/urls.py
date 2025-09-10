from django.urls import path
from . import views
from .views import list_books
from django.urls import path
from .views import list_books, LibraryDetailView, register_view, login_view, logout_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Existing app views
    path("books/", views.list_books, name="list_books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Authentication routes
    path("register/", views.register, name="register"),  # ✅ explicit FBV

    path(
        "login/",
        LoginView.as_view(template_name="relationship_app/login.html"),
        name="login"
    ),  # ✅ required CBV

    path(
        "logout/",
        LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout"
    ),  # ✅ required CBV
]

