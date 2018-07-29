from django.conf.urls import url
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views


app_name = "egamen"


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^story/(?P<story_id>[0-9]+)/page/(?P<page>[0-9]+)/$', views.post, name="post_chapter"),
    url(r'^story/(?P<story_id>[0-9]+)/comments/(?P<page>[0-9]+)/$', views.commentList, name="comments"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login_user.html'), name='login'),
    url(r'^register/$', views.register_user, name="register"),
    url(r'^user/$', views.user_profile, name='profile'),
    url(r'^user/add/story/$', views.add_story, name='addstory'),
    url(r'^user/edit/story/(?P<pk>[0-9]+)/$', views.EditStory.as_view(), name="edit_story"),
    url(r'^user/edit/(?P<id>[0-9]+)/chapter/$', views.manageChapter, name="edit_chapter"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^user/delete/story/(?P<id>[0-9]+)/$', views.delete_story, name="delete_story"),
    url(r'^profile/(?P<username>[\w]+)/$', views.userStories, name="userstories"),
    url(r'^about/$', views.about, name="about"),
    url(r'^404/$', views.handle_404, name="web404"),
    url(r'^search/$', views.search, name="search"),




]


