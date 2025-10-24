from django.urls import path, include
from django.contrib import admin
from .views import ToggleLikeView, PostLikesView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostCommentListView, PostCommentDetailView, PostCommentCreateView, PostCommentUpdateView, PostCommentDeleteView 

urlpatterns = [
    path('posts/<int:pk>/like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('posts/<int:pk>/post_likes/', PostLikesView.as_view(), name='post-likes'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:post_id>/comments/', PostCommentListView.as_view(), name='comment-list'),
    path('posts/<int:post_id>/comments/<int:pk>/', PostCommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:post_id>/comments/create/', PostCommentCreateView.as_view(), name='comment-create'),
    path('posts/<int:post_id>/comments/<int:pk>/update/', PostCommentUpdateView.as_view(), name='comment-update'),
    path('posts/<int:post_id>/comments/<int:pk>/delete/', PostCommentDeleteView.as_view(), name='comment-delete'),
]