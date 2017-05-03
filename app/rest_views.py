from . import serializers
import logging

from django.contrib.auth import authenticate, login
from rest_framework import permissions, authentication, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from friendship.models import Friend
from . models import User

logger = logging.getLogger('friend_finder')


class FriendList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FriendSerializer

    def get_queryset(self):
        return Friend.objects.friends(self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


@api_view(["GET", "POST", ])
@permission_classes((permissions.AllowAny,))
def friends(request):
    if request.method == 'POST':
        try:
            friend_data = request.data
            other_user = User.objects.get(username=friend_data['username'])

            if Friend.objects.are_friends(request.user, other_user):
                return Response({"message": "Already friends"}, status=status.HTTP_400_BAD_REQUEST)

            Friend.objects.add_friend(
                request.user,  # The sender
                other_user,  # The recipient
                message='Hi! I would like to add you')  # This message is optional

            return Response({"message": "Friend request sent"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Friend request failed"}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUser(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return get_user_model().objects.get(email=self.request.user.email)


class OtherUser(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        if "uid" in self.kwargs and self.kwargs["uid"]:
            users = get_user_model().objects.filter(id=self.kwargs["uid"])
        elif "email" in self.kwargs and self.kwargs["email"]:
            users = get_user_model().objects.filter(email=self.kwargs["email"])
        else:
            users = None
        if not users:
            self.other = None
            raise exceptions.NotFound
        self.other = users[0]
        return self.other

    def get_serializer_class(self):
        if self.request.user == self.other:
            return serializers.UserSerializer
        else:
            return serializers.FriendSerializer


class UpdatePosition(generics.UpdateAPIView):
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdatePosition, self).dispatch(*args, **kwargs)

    def get_object(self):
        return get_user_model().objects.get(email=self.request.user.email)

    def perform_update(self, serializer, **kwargs):
        try:
            geo_data = self.request.data
            lat = geo_data["lat"]
            lon = geo_data["lon"]
            if lat and lon:
                point = Point(lon, lat)
            else:
                point = None

            logger.info('Location: ' + str(lat) + ',' + str(lon))

            if point:
                serializer.save(last_location = point)
            return serializer
        except:
            pass


@api_view(["POST", ])
@permission_classes((permissions.AllowAny,))
def token_login(request):
    login_data = request.data
    username = login_data["username"]
    password = login_data["password"]

    if (not username) or (not password):
        return Response({"detail": "Missing username and/or password"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            try:
                my_token = Token.objects.get(user=user)
                return Response({"token": "{}".format(my_token.key)}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": "Could not get token"})
        else:
            return Response({"detail": "Inactive account"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Invalid User Id of Password"}, status=status.HTTP_401_UNAUTHORIZED)
