from django.db import models 
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):

    def get_by_natural_key(self, username):
        return self.get(
            models.Q(**{self.model.USERNAME_FIELD: username}) |
            models.Q(**{self.model.EMAIL_FIELD: username})
        )

class User(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CustomUserManager()
    following = models.ManyToManyField(
        'self', through='Follow', symmetrical=False, related_name='followers'
    )
    def follow(self, target_user):
        if self == target_user:
            raise ValueError("You cannot follow yourself.")

        if not self.is_following(target_user):
            Follow.objects.create(follower=self, following=target_user)
            return True
        return False

    def unfollow(self, target_user):
        if self.is_following(target_user):
            Follow.objects.filter(follower=self, following=target_user).delete()
            return True
        return False

    def is_following(self, target_user):
        return Follow.objects.filter(follower=self, following=target_user).exists()

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    # is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username



class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower','following'],  name="unique_followers"),
            models.CheckConstraint(check=~models.Q(follower=models.F("following")), name="no_self_follow")
        ]
        ordering = ["-created_at"]
        
    def __str__(self) -> str:
        return f"{self.follower} follows {self.following}"