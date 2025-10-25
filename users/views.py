from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView, generics
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Profile, Follow
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.
# User Registration View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user) #retrieves token if exists and create a new one if it doesn't
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# User Login View
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Profile View for viewing and updating user profile
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request): # get the profile of the authenticated user
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request): # update the profile of the authenticated user
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

#list all users(public info only)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # allow anyone to view the user list
    
#retrieve specific user details
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # allow anyone to view user details
    

#-----------------Follow/Unfollow views--------------------------
#view to follow a user
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try: #find user to follow
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        #prevent users from following themselves
        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        #create follow relationship if none    
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)    
        
        if not created: #already following
            return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": f"You are now following {target_user.username}."}, status=status.HTTP_201_CREATED)#follow successful
#view to unfollow a user    
class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated] #only logged in users can unfollow

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            follow = Follow.objects.get(follower=request.user, following=target_user)
            follow.delete() #unfollow the user
            return Response({"detail": f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:#no follow relationship exists
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

#---------------------------following/follower lists-------------------------
class FollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return User.objects.filter(following__following__id=user_id)  # users who follow the target user
    

class FollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return User.objects.filter(followers__follower__id=user_id)  # users whom the target user follows