from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^$', views.Landing.as_view(), name='landing'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^userprofile/$', views.UserProfile.as_view(success_url="/friend-finder/userprofile/"), name='userprofile'),
    url(r'^friends/$', views.add_friend_view, name='friends')
]
