from django.core.validators import (MinValueValidator,
                                    MaxValueValidator)
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    objects = None
    title = models.CharField(max_length=128, verbose_name='title')
    description = models.TextField(max_length=2048,
                                   blank=True,
                                   verbose_name='description')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def has_review(self):
        return self.review_set.exists()

    @property
    def review(self):
        return self.review_set.first()


class Review(models.Model):
    objects = None
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    objects = None
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)
