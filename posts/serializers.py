from rest_framework import serializers
from .models import Post, Comment, Like

#post serializer converts model instances to JSON and validates input data
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at'] #prevents clients from modifying these fields
        
#comment serializer handles serialization and validation for comments
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id') #include post id in comment representation
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at'] #prevents clients from modifying these fields
       
#like serializer shows who liked which post
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.id')
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at'] #prevents clients from modifying these fields
        
        
        