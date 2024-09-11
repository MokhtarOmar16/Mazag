from django.db import models 
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)



class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, related_name='data')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

    def follow(self, user):
        if self.is_following(user):
            return 
        return Follow.objects.create(user=user, follower_user=self)


    def is_following(self, user):
        return Follow.objects.filter(user=user, follower_user=self).exists()


    def unfollow(self, user):
        if self.is_following(user):
            return
        return Follow.objects.delete(user=user, follower_user=self)


class Follow(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    follower_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]
        ordering = ["-created_at"]
        
    def __str__(self) -> str:
        return f"{self.follower_user} follows {self.user}"