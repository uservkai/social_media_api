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
    
#------------------COMMENT VIEWS---------------------
#List all comments for a post
class CommentListView(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    
#retrieve a single comment
class CommentDetailView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    
#Create a new comment
class CommentCreateView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):#auto set author as the logged in user
        serializer.save(author=self.request.user)
        
#update a comment
class CommentUpdateView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)#only author can update comment
        
#delete a comment
class CommentDeleteView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
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
 
     