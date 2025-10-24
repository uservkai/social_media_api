from django.urls import path, include
from django.contrib import admin
from .views import ToggleLikeView, PostLikesView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentListView, CommentDetailView, CommentCreateView, CommentUpdateView, CommentDeleteView 

urlpatterns = [
    path('posts/<int:pk>/like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('posts/<int:pk>/post_likes/', PostLikesView.as_view(), name='post-likes'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]