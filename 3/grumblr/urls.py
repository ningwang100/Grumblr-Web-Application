from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'grumblr.views.home'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'grumblr/login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^register$', 'grumblr.views.register',name='register'),
    url(r'^MyProfile$', 'grumblr.views.myProfile',name='myProfile'),
    url(r'^OtherProfile/(?P<uid>\d+)$', 'grumblr.views.other_profile',name='otherProfile'),
    url(r'^add-post$', 'grumblr.views.add_post',name='add'),
    url(r'^search$', 'grumblr.views.search',name='search'),
    url(r'^editProfile$', 'grumblr.views.edit_profile',name='edit'),

]