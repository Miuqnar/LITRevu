from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLES_CHOICES = (
        (CREATOR, 'Createur'),
        (SUBSCRIBER, 'Abonné'),
    )

    profile_photo = models.ImageField(verbose_name='Photo de profile')
    role = models.CharField(max_length=30, choices=ROLES_CHOICES, verbose_name='Rôle')
    
    # def following(self):
    #     return self.following.all()
    
    # def followed_by(self):
    #     return self.followed_by.all()
        