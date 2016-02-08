from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from grumblr.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from grumblr.forms import *
from mimetypes import guess_type
from django.db import transaction
from time import time
import pytz
from datetime import datetime
from pytz import timezone

@transaction.atomic
def judge_login(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return redirect(reverse('login'))


def global_stream(request, args):
    context = {}
    newUser = UserProfile.objects.get(user=request.user)
    followers = UserProfile.objects.filter(user__in=request.user.newuser.follow.all()).reverse()
    unfollowers = UserProfile.objects.exclude(user__in=request.user.newuser.follow.all()).reverse()
    context['home'] = 'grumblr/global_stream.html'
    context['addPost'] = PostForm()
    context['posts'] = Grumblr.objects.all().order_by("time").reverse()
    context['newUser'] = newUser
    context['searchForm'] = SearchForm()
    context['followers'] = followers
    context['unfollowers'] = unfollowers
    context['update_time'] = time()
    for key in args.keys():
        context[key] = args[key]
    global login_user
    login_user = User.objects.get(username=request.user.username)
    context['stream'] = 'globalUpdate'
    return render(request, context['home'], context)


@login_required
@transaction.atomic
def home(request):
    return global_stream(request, {})


@login_required
def update_global_stream(request):
    if not 'time' in request.GET or not request.GET['time']:
        return HttpResponse('error')

    last_update = datetime.fromtimestamp(float(request.GET['time']),pytz.UTC)
    json = {'update_time': time()}
    grumblrs = []

    new_grumblr = Grumblr.objects.filter(time__gt=last_update).order_by('time')

    eastern = timezone('US/Eastern')
    fmt = '%b. %d, %Y, %I:%M %p.'
    for grumblr in new_grumblr:
        g = {}
        if grumblr.user in request.user.newuser.follow.all():
            g['myfollower'] = 'myFollower'
        else:
            g['myfollower'] = 'notFollower'

        g['gid'] = grumblr.id
        g['user_id'] = grumblr.user.id
        g['user_username'] = grumblr.user.username
        loc_time = grumblr.time.astimezone(eastern)
        g['time'] = loc_time.strftime(fmt)
        g['content'] = grumblr.content
        grumblrs.append(g)

    json['grumblrs'] = grumblrs
    return JsonResponse(json)


def send_email(request):
    context = {}
    if request.method == "GET":
        context['emailForm'] = SendEmailForm()
        return render(request, 'grumblr/sendEmail.html', context)

    emailForm = SendEmailForm(request.POST)
    context['emailForm'] = emailForm

    if not emailForm.is_valid():
        return render(request, 'grumblr/sendEmail.html', context)

    email = emailForm.cleaned_data['email']
    user = User.objects.get(email=email)
    token = default_token_generator.make_token(user)
    message = "Send an email successfully"
    context['message'] = message
    send_mail(subject="Reset your grumblr password",
              message="Please visit http://127.0.0.1:8000/reset?token=%s to reset your new password." % token,
              from_email="ningw@andrew.cmu.edu",
              recipient_list=[email])
    userInfo = UserProfile.objects.get(user__exact=user)
    userInfo.token = token
    userInfo.save()
    return render(request, 'grumblr/sendEmail.html', context)


def resetPwd(request):
    context = {}
    if request.method == "GET":
        context['resetForm'] = resetForm()
        token = request.GET['token']
        context['token'] = token
        return render(request, 'grumblr/resetPassword.html', context)
    if request.method == "POST":
        ResetForm = resetForm(request.POST)
        context['resetForm'] = ResetForm
        token = request.POST['token']
        context['token'] = token

    if not ResetForm.is_valid():
        return render(request, 'grumblr/resetPassword.html', context)

    user = UserProfile.objects.get(token=token).user
    user.set_password(ResetForm.cleaned_data['password1'])
    user.save()
    context['msg'] = "Your new password has been setted successfully."
    return redirect('/')


@login_required
@transaction.atomic
def myProfile(request):
    context = {}
    newUser = UserProfile.objects.get(user=request.user)
    global login_user
    login_user = User.objects.get(username=request.user.username)
    followers = UserProfile.objects.filter(user__in=request.user.newuser.follow.all()).reverse()
    context = {'posts': Grumblr.objects.filter(user__exact=request.user).order_by("time").reverse(),
               'newUser': newUser, 'login_user': login_user, 'followers': followers, 'stream': 'other'}
    return render(request, 'grumblr/profile.html', context)


@login_required
@transaction.atomic
def add_post(request):
    context = {}
    if request.method == 'GET':
        context['addPost'] = PostForm()
        return global_stream(request,context)

    addPost = PostForm(request.POST)
    context['addPost'] = addPost

    if not addPost.is_valid():
        return global_stream(request, context)

    new_post = Grumblr(user=request.user, content=addPost.cleaned_data['content'])
    new_post.save()
    newUser = UserProfile.objects.get(user=request.user)

    context['newUser'] = newUser
    context['addPost'] = PostForm()
    return global_stream(request, context)


@login_required
@transaction.atomic
def other_profile(request, uid):
    context={}
    try:
        user = User.objects.get(id__exact=uid)
    except User.DoesNotExist:
        context['errors'] = ['This user Id is invalid']
        return global_stream(request, context)

    newUser = UserProfile.objects.get(user=user)
    posts = Grumblr.objects.filter(user__exact=user).order_by('-time')
    global login_user
    login_user = User.objects.get(username=request.user.username)
    followers = UserProfile.objects.filter(user__in=request.user.newuser.follow.all()).reverse()
    context = {'user': user, 'posts': posts, 'newUser': newUser, 'login_user': login_user, 'followers': followers,
               'stream': 'globalUpdate'}

    if request.user.id == user.id:
        return render(request, 'grumblr/profile.html', context)
    else:
        context = {'user': user, 'posts': posts, 'newUser': newUser,
                   'login_user': login_user, 'following': user in request.user.newuser.follow.all(), 'stream': 'globalUpdate'}
        return render(request, 'grumblr/profile.html', context)


@login_required
@transaction.atomic
def search(request):
    errors = []
    form = SearchForm(request.GET)
    posts = Grumblr.objects.all().order_by('-time')
    followers = UserProfile.objects.filter(user__in=request.user.newuser.follow.all()).reverse()
    unfollowers = UserProfile.objects.exclude(user__in=request.user.newuser.follow.all()).reverse()
    context = {'posts': posts, 'errors': errors, 'searchForm': form, 'addPost': PostForm(),
               'followers': followers, 'unfollowers': unfollowers, 'stream': 'globalUpdate'}
    if not form.is_valid():
        errors.append('Keyword is required.')
        return render(request, 'grumblr/global_stream.html', context)
    else:
        keyword = form.cleaned_data['keyword']
        posts = Grumblr.objects.filter(content__contains=request.GET['keyword']).order_by('-time')
        if len(posts) == 0:
            errors.append("No posts matched the keyword.")
            return render(request, 'grumblr/global_stream.html', context)
        context['keyword'] = keyword
        context['posts'] = posts
        return global_stream(request, context)


@login_required
@transaction.atomic
def edit_profile(request):
    context = {}
    errors = []
    context['user'] = request.user
    newUser = UserProfile.objects.get(user=request.user)
    context['newUser'] = newUser
    context['editForm'] = EditForm(initial={'first_name': request.user.first_name,
                                            'last_name': request.user.last_name,
                                            'email': request.user.email,
                                            'age': newUser.age})
    if request.method == 'GET':
        return render(request, 'grumblr/EditProfile.html', context)
    form = EditForm(request.POST, request.FILES)
    context['editForm'] = form
    if not form.is_valid():
        return render(request, 'grumblr/EditProfile.html', context)

    if not len(User.objects.exclude(id=request.user.id).filter(email=request.POST['email'])) == 0:
        errors.append('Email is registered.')

    if errors:
        context['errors'] = errors
        return redirect('grumblr/editProfile')

    if form.cleaned_data['email']:
        request.user.email = form.cleaned_data['email']
    if form.cleaned_data['first_name']:
        request.user.first_name = form.cleaned_data['first_name']
    if form.cleaned_data['last_name']:
        request.user.last_name = form.cleaned_data['last_name']
    if form.cleaned_data['age']:
        newUser.age = form.cleaned_data['age']
    if form.cleaned_data['avatar']:
        new_avatar = form.cleaned_data['avatar']
        newUser.avatar = new_avatar

    bio = newUser.bio
    if form.cleaned_data['self_bio']:
        bio = form.cleaned_data['self_bio']
    newUser.bio = bio

    oldPassword = form.cleaned_data['oldPassword']
    if form.cleaned_data['oldPassword'] != "":
        if not request.user.check_password(oldPassword):
            errors.append('Old password is not correct.')
            context['errors'] = errors
            update_session_auth_hash(request, request.user)
            return render(request, 'grumblr/EditProfile.html', context)
        else:
            request.user.set_password(form.cleaned_data['password1'])
            request.user.save()
            return redirect('/')

    request.user.save()
    newUser.save()
    context['msg'] = "Your new profile is saved."
    global login_user
    login_user = User.objects.get(username=request.user.username)
    return render(request, 'grumblr/EditProfile.html', context)


@login_required
@transaction.atomic
def follow(request, uid):
    try:
        user = User.objects.get(id__exact=uid)
    except User.DoesNotExist:
        return HttpResponse("This user does not exist")

    newUser = UserProfile.objects.get(user=user)
    posts = Grumblr.objects.filter(user__exact=user).order_by('-time')
    global login_user
    login_user = User.objects.get(username=request.user.username)
    context = {'user': user, 'posts': posts, 'newUser': newUser, 'login_user': login_user, 'stream': 'other'}
    if uid == request.user.id:
        return redirect('/OtherProfile/' + uid)

    if user in request.user.newuser.follow.all():
        request.user.newuser.follow.remove(user)
    else:
        request.user.newuser.follow.add(user)

    request.user.save()
    newUser.save()
    context['user'] = user
    return redirect('/OtherProfile/' + uid)


@login_required
@transaction.atomic
def my_follower(request):
    context = {}
    newUser = UserProfile.objects.get(user=request.user)
    unfollowers = UserProfile.objects.exclude(user__in=request.user.newuser.follow.all()).reverse()
    context['addPost'] = PostForm()
    followers = UserProfile.objects.filter(user__in=request.user.newuser.follow.all()).reverse()
    context['posts'] = Grumblr.objects.filter(user__in=request.user.newuser.follow.all()).order_by("time").reverse()
    context['newUser'] = newUser
    context['searchForm'] = SearchForm()
    context['followers'] = followers
    context['unfollowers'] = unfollowers
    context['stream'] = "Follower"
    context['update_time'] = time()
    global login_user
    login_user = User.objects.get(username=request.user.username)
    return render(request, 'grumblr/follower.html', context)


@login_required
@transaction.atomic
def get_avatar(request, uid):
    context={}
    try:
        newUser = UserProfile.objects.get(user_id=uid)
    except UserProfile.DoesNotExist:
        context['errors'] = ['This user Id is invalid. Thus can not found the avatar!']
        return global_stream(request, context)

    if not newUser.avatar:
        return HttpResponse('not this avatar')

    content_type = guess_type(newUser.avatar.name)
    return HttpResponse(newUser.avatar, content_type=content_type)


def register(request):
    context = {'registerForm': RegisterForm()}
    if request.method == 'GET':
        return render(request, 'grumblr/register.html', context)

    form = RegisterForm(request.POST, request.FILES)
    context['registerForm'] = form

    if not form.is_valid():
        return render(request, 'grumblr/register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])
    new_user.save()

    newUser = UserProfile.objects.create(user=new_user,
                                         age=form.cleaned_data['age'],
                                         avatar=form.cleaned_data['avatar'])
    newUser.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)

    return redirect('/')


@login_required
def obtain_comment(request,gid):
    context={}
    try:
        post = Grumblr.objects.get(id__exact=gid)
    except Grumblr.DoesNotExist:
        context['errors'] = ['This post does not exist']
        return global_stream(request, context)

    eastern = timezone('US/Eastern')
    Comments = post.comments.order_by('timestamp')
    fmt = '%b. %d, %Y, %I:%M %p.'
    json = {}
    json['comments']=[]
    for Comment in Comments:
        loc_time = Comment.timestamp.astimezone(eastern)
        comment = {'userId':Comment.user.id,
                   'username':Comment.user.username,
                   'timestamp':loc_time.strftime(fmt),
                   'content':Comment.comment}
        json['comments'].append(comment)
    return JsonResponse(json)


@login_required
def reply_comment(request):
    if request.method == 'GET':
        return HttpResponse("Please add comments by POST method.")

    form = CommentForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Please say something.")
    # if not 'text' in request.POST or not request.POST['text']:
    #     return HttpResponse("Please say something.")

    if not 'grumblr_id' in request.POST or not request.POST['grumblr_id']:
        return HttpResponse("The gid is not provided.")

    if not Grumblr.objects.filter(id__exact=request.POST['grumblr_id']):
        return HttpResponse("The grumblr does not exist.")

    post = Grumblr.objects.get(id__exact=request.POST['grumblr_id'])
    new_comment = Comment(user=request.user, comment=request.POST['text'],post=post)
    new_comment.save()

    return HttpResponse("success")