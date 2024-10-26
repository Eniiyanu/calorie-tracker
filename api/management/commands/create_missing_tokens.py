# api/management/commands/create_missing_tokens.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Create auth tokens for existing users who don\'t have them'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        tokens_created = 0
        tokens_existing = 0

        for user in users:
            
            token, created = Token.objects.get_or_create(user=user)
            if created:
                tokens_created += 1
            else:
                tokens_existing += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Tokens: {tokens_created} created, {tokens_existing} already existed'
            )
        )
