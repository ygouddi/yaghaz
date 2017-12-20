from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views


app_name = "egamen"


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^story/(?P<id>[0-9]+)/$', views.chapter, name="post"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login_user.html'), name='login'),
    url(r'^register/$', views.register_user, name="register"),
    url(r'^user/$', views.user_profile, name='profile'),
    url(r'^user/add/story/$', views.add_story, name='addstory'),
    url(r'^user/edit/story/(?P<pk>[0-9]+)/$', views.EditStory.as_view(), name="edit_story"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

]