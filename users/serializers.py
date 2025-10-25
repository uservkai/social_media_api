from rest_framework import serializers
from .models import User, Profile, Follow
from django.contrib.auth import authenticate

# converts user registration data to JSON and creates new user instances
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user)  # auto-create an associated profile
        return user

#converts user login data to JSON and validates credentials  
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=20, write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

# converts profile model instances to JSON allowing authenticated users to view and update their profile information
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture', 'location')

class UserSerializer(serializers.ModelSerializer):
    # nested profile serializer to include in output
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    mutual_friends = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'follower_count', 'following_count', 'mutual_friends')
        
    def get_follower_count(self, obj): #count of followers
        return obj.followers.count()
    
    def get_following_count(self, obj): #count of users this user is following
        return obj.following.count()
    
    def get_mutual_friends(self, obj): #get users following this user
        followers = set(obj.followers.values_list('follower_id', flat=True))
        #ids this user is following
        following = set(obj.following.values_list('following_id', flat=True))
        
        #intexection
        mutuals = followers.intersection(following)
        return len(mutuals)
        
        
