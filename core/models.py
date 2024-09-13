from django.db import models 
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import UserManager
from django.db.models import Q

class CustomUserManager(UserManager):

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )



class User(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CustomUserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, related_name='data')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

    def follow(self, pk):
        following = self.is_following(pk)
        if not following:
            Follow.objects.create(user_id=pk, follower_user=self)
        return following

    def is_following(self, pk):
        return Follow.objects.filter(user_id=pk, follower_user=self).exists()


    def unfollow(self, pk):
        following =  self.is_following(pk)
        if following:
            Follow.objects.filter(user_id=pk, follower_user=self).delete()
        return following


class Follow(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    follower_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','follower_user_id'],  name="unique_followers")
        ]
        ordering = ["-created_at"]
        
    def __str__(self) -> str:
        return f"{self.follower_user} follows {self.user}"