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


class Friend(models.Model):
    class Meta:
        verbose_name = "friends"
        verbose_name_plural = "friends"

    # All friends of current user
    users = models.ManyToManyField(
        User
    )
    # Owner of friend list
    current_user = models.ForeignKey(
        User,
        related_name='owner',
        null=True
    )

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
