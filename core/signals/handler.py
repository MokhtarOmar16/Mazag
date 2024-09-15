from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import UserProfile, Follow
from django.core.exceptions import ValidationError



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])



@receiver(post_save, sender=Follow)
def update_follow_count_on_follow(sender, instance, created, **kwargs):
    if created:
        if instance.follower == instance.following:
            raise ValidationError("You cannot follow yourself.")
        instance.follower.profile.following_count += 1
        instance.following.profile.followers_count += 1
        instance.follower.profile.save()
        instance.following.profile.save()

@receiver(post_delete, sender=Follow)
def update_follow_count_on_unfollow(sender, instance, **kwargs):
    instance.follower.profile.following_count -= 1
    instance.following.profile.followers_count -= 1
    instance.follower.profile.save()
    instance.following.profile.save()
