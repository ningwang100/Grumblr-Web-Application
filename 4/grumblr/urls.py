from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'grumblr.views.home'),
    url(r'^unlogin$', 'django.contrib.auth.views.login', {'template_name':'grumblr/login.html'},name="login"),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^register$', 'grumblr.views.register',name='register'),
    url(r'^MyProfile$', 'grumblr.views.myProfile',name='myProfile'),
    url(r'^OtherProfile/(?P<uid>\d+)$', 'grumblr.views.other_profile',name='otherProfile'),
    url(r'^media/avatar/(?P<uid>\d+)$', 'grumblr.views.get_avatar', name = 'getAvatar'),
    url(r'^add-post$', 'grumblr.views.add_post',name='add'),
    url(r'^search$', 'grumblr.views.search',name='search'),
    url(r'^editProfile$', 'grumblr.views.edit_profile',name='edit'),
    url(r'^follow/(?P<uid>\d+)$', 'grumblr.views.follow'),
    url(r'^myFollower/$','grumblr.views.my_follower',name='follower'),
    url(r'^login/$','grumblr.views.judge_login',name ="judge_login"),
    url(r'^sendEmail/$','grumblr.views.send_email',name = "send"),
     url(r'^reset/$','grumblr.views.resetPwd',name = "reset")
]