from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    last_location = models.PointField(
        verbose_name="last known location",
        blank=True,
        default='SRID=4326;POINT(53.3498 -6.2603)'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return "{}, ({}), last seen at {} ... cr={}, mod={}" \
            .format(self.username, self.get_full_name(), self.last_location, self.created, self.modified)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
