from django.conf.urls import url, include
from django.contrib.gis import admin
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url('friend-finder/', include('app.urls', namespace="app")),
    url(r'^api/', include('app.rest_urls', namespace="api")),
    url(r'^friendship/', include('friendship.urls'))
]
