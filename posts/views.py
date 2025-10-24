from django.shortcuts import render
from rest_framework import viewsets, permissions, status,filters
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

# Create your views here.
#------------------POST VIEWS---------------------
#List all posts
class PostListView(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Post.objects.all().annotate(
            like_count=Count('likes'),
            comment_count=Count('comments')
        ).order_by('-created_at', '-like_count', '-comment_count')
        
    #filtering, searching, ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['author__username', 'created_at']
    search_fields = ['author__username', 'content'] 
    ordering_fields = ['created_at', 'updated_at', 'author__username','like_count', 'comment_count']
    
#view/retrieve a single post
class PostDetailView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    
#Createa a new post
class PostCreateView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):#auto set author as the logged in user
        serializer.save(author=self.request.user)

#update a post
class PostUpdateView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)#only author can update post

#delete a post
class PostDeleteView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
#------------------COMMENT VIEWS(comments are nested in posts)---------------------
#List all comments for a post
class PostCommentListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id'] #filter comments by post id from URL
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')
    
#retrieve a single comment under a post
class PostCommentDetailView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)
    
#Create comment on a post
class PostCommentCreateView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):#auto set author as the logged in user
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)
        
#update a comment
class PostCommentUpdateView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, author=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)#only author can update comment
        
#delete a comment under a post
class PostCommentDeleteView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, author=self.request.user)
    
#------------------LIKE VIEWS---------------------
#handle post like/unlike functionality - a toggle allowing auth users to like, unlike / undo like unlike
class ToggleLikeView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer
    
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        #check if user already liked the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            #user already liked the post, so unlike it
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        
        #new like created
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)

#List all likes for a post; displays liked-by info
class PostLikeListView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id'] #filter likes by queryset
        return Like.objects.filter(post__id=post_id. order_by('-created_at'))
 
     