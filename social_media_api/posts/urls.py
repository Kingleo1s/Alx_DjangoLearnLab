from django.urls import path
from .views import PostListCreateView, CommentListCreateView, FeedView
from django.urls import path
from .views import LikePostView, UnlikePostView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]
