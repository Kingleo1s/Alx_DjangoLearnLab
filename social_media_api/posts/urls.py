from django.urls import path
from .views import PostListCreateView, CommentListCreateView, FeedView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('feed/', FeedView.as_view(), name='feed'),
]
