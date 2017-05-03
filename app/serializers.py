from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from friendship.models import FriendshipRequest


class UserSerializer(geo_serializers.GeoFeatureModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        geo_field = "last_location"
        fields = (
            "id", "username", "first_name", "last_name", "email", "is_superuser", "is_staff",
            "is_active", "date_joined", "last_login", "url", "modified")

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(reverse("api:user-username", kwargs={"uid": obj.pk}))


class FriendSerializer(geo_serializers.GeoFeatureModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        geo_field = "last_location"
        fields = ("id", "username", "first_name", "last_name", "email", "url", "modified")

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(reverse("api:user-username", kwargs={"uid": obj.pk}))


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
