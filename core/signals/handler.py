from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import UserProfile, Follow

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


@receiver(post_save, sender=Follow)
def increase_follow_count(sender, instance, created, **kwargs):
    if created: 
        instance.follower.following_count += 1
        instance.follower.save()

        instance.following.followers_count += 1
        instance.following.save()

@receiver(post_delete, sender=Follow)
def decrease_follow_count(sender, instance, **kwargs):
        instance.follower.following_count -= 1
        instance.follower.save()

        instance.following.followers_count -= 1
        instance.following.save()
