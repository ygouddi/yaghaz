from django.conf.urls import url,include
from django.contrib import admin
from . import views


app_name = "egamen"


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^story/(?P<story_id>[0-9]+)/$', views.chapter, name="post"),
    url(r'^login/$', views.login_user, name="login"),
    url(r'^register/$', views.register_user, name="register"),
    url(r'^logout_user/$', views.logout_user, name="logout_user"),
]