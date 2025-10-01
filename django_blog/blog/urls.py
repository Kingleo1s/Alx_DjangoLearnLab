
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "blog"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),

    # Login / Logout using Django's built-in views
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logged_out.html"), name="logout"),
    path("", views.home, name="home"),   # this makes {% url 'blog:home' %} work
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path("posts/", views.post_list, name="posts")
]
