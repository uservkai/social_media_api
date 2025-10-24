from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
# custom user model extending AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

# profile model to extend user information 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='images/', blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile" 
 
 #follow model to represent follower-following relationships   
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following') # prevent duplicate follows

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
