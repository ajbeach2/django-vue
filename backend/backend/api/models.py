from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class BaseModel(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        abstract = True


class Profile(BaseModel):
    """User Profiles."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    email_confirmed = models.BooleanField(blank=False, default=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
