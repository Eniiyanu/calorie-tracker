from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

def create_user_token(user):
    """Create or get auth token for a user"""
    token, created = Token.objects.get_or_create(user=user)
    return token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        create_user_token(instance)