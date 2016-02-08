from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from django.conf import settings

urlpatterns = [
    url(r'^$', 'grumblr.views.home',name="home"),
    url(r'^unlogin$', 'django.contrib.auth.views.login', {'template_name':'grumblr/login.html'},name="login"),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^register$', 'grumblr.views.register',name='register'),
    url(r'^MyProfile$', 'grumblr.views.myProfile',name='myProfile'),
    url(r'^OtherProfile/(?P<uid>\d+)$', 'grumblr.views.other_profile',name='otherProfile'),
    url(r'^media/avatar/(?P<uid>\d+)$', 'grumblr.views.get_avatar', name = 'getAvatar'),
    url(r'^add-post$', 'grumblr.views.add_post',name='add'),
    url(r'^search$', 'grumblr.views.search',name='search'),
    url(r'^editProfile$', 'grumblr.views.edit_profile',name='edit'),
    url(r'^follow/(?P<uid>\d+)$', 'grumblr.views.follow',name='follow'),
    url(r'^myFollower/$','grumblr.views.my_follower',name='follower'),
    url(r'^login/$','grumblr.views.judge_login',name ="judge_login"),
    url(r'^sendEmail/$','grumblr.views.send_email',name = "send"),
    url(r'^reset/$','grumblr.views.resetPwd',name = "reset"),
    url(r'^update-global-stream$','grumblr.views.update_global_stream',name="updateGlobalStream"),
    url(r'^reply-comment$','grumblr.views.reply_comment',name="reply"),
    url(r'^get-comment/(?P<gid>\d+)$','grumblr.views.obtain_comment',name="getcomment")
]
urlpatterns += staticfiles_urlpatterns()
