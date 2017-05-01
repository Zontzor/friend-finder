from django.conf.urls import include, url

from . import rest_views

urlpatterns = [
    url(r'^tokenlogin/$', rest_views.token_login, name='token-login'),
    url(r'^userme/$', rest_views.CurrentUser.as_view(), name='user-me'),
    url(r'^friendlist/$', rest_views.FriendList.as_view(), name='friendlist'),
    url(r'^user/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', rest_views.OtherUser.as_view(), name='user-email'),
    url(r'^user/(?P<uid>\d+)/$', rest_views.OtherUser.as_view(), name='user-username'),
    url(r'^position/$', rest_views.UpdatePosition.as_view(), name='update-position'),
    url(r'^friends/$', rest_views.friends, name='friends'),
]
