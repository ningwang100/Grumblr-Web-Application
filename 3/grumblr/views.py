from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from grumblr.models import *


@login_required
def home(request):
    context = {}
    newUser = UserProfile.objects.get(user=request.user)
    context['posts'] = Grumblr.objects.all().order_by("time").reverse()
    context['newUser'] = newUser
    global login_user
    login_user = User.objects.get(username=request.user.username)
    return render(request, 'grumblr/global_stream.html', context)

@login_required
def myProfile(request):
    newUser = UserProfile.objects.get(user=request.user)
    context = {'grumblrs': Grumblr.objects.filter(user__exact=request.user).order_by("time").reverse(),
               'newUser': newUser,'login_user':login_user}
    return render(request, 'grumblr/profile.html', context)

@login_required
def add_post(request):
    errors = None
    if not 'text' in request.POST or not request.POST['text']:
        errors = 'You must enter something.'
    else:
        if len(request.POST['text']) > 42:
            errors = 'You post message need to 42 characters or less.'
            context = {'posts': Grumblr.objects.all().order_by('-time')}
            context['add_post_errors'] = errors
            return render(request, 'grumblr/global_stream.html', context)
        else:
            new_post = Grumblr(user=request.user, content=request.POST['text'])
            new_post.save()
    newUser = UserProfile.objects.get(user=request.user)
    context = {'posts': Grumblr.objects.all().order_by('-time')}
    context['add_post_errors'] = errors
    context['newUser'] = newUser
    return render(request, 'grumblr/global_stream.html', context)

@login_required
def other_profile(request, uid):
    user = User.objects.get(id__exact=uid)
    newUser = UserProfile.objects.get(user=user)
    grumblrs = Grumblr.objects.filter(user__exact=user).order_by('-time')
    global login_user
    context = {'user': user, 'grumblrs': grumblrs, 'newUser': newUser, 'login_user': login_user}
    return render(request, 'grumblr/profile.html', context)

@login_required
def search(request):
    errors = []
    posts = Grumblr.objects.exclude(user__exact=request.user).order_by('-time')

    if not 'keyword' in request.GET or not request.GET['keyword']:
        errors.append('Keyword is required.')
        return render(request, 'grumblr/global_stream.html', {'posts': posts, 'errors': errors})
    else:
        posts = Grumblr.objects.filter(content__contains=request.GET['keyword']).order_by('-time')
        return render(request, 'grumblr/global_stream.html', {'posts': posts, 'keyword': request.GET['keyword']})

@login_required
def edit_profile(request):
    context = {}
    context['user'] = request.user
    newUser = UserProfile.objects.get(user=request.user)
    context['newUser'] = newUser
    # just display the profile fields if this is a GET request
    if request.method == 'GET':
        return render(request, 'grumblr/EditProfile.html', context)

    errors = []
    context['errors'] = errors

    if not 'email' in request.POST or not request.POST['email']:
        errors.append('Email is required.')
    elif not len(User.objects.exclude(id__exact=request.user.id).filter(email__iexact=request.POST['email'])) == 0:
        errors.append('Email is registered.')

    if not 'firstname' in request.POST or not request.POST['firstname']:
        errors.append('First Name is required.')

    if not 'lastname' in request.POST or not request.POST['lastname']:
        errors.append('Last Name is required.')

    if 'old' in request.POST and request.POST['old']:
        if not 'password1' in request.POST or not request.POST['password1']:
            errors.append('New password is required.')
        if not 'password2' in request.POST or not request.POST['password2']:
            errors.append('Confirm new password is required.')
        if not request.user.check_password(request.POST['old']):
            errors.append('Old password is not correct')

    if errors:
        return render(request, 'grumblr/EditProfile.html', context)

    request.user.email = request.POST['email']
    request.user.first_name = request.POST['firstname']
    newUser.photopath = request.POST['lastname']
    if 'old' in request.POST and request.POST['old']:
        request.user.set_password(request.POST['password1'])
    request.user.save()
    newUser.save()
    context['msg'] = "Your new profile is saved."
    return render(request, 'grumblr/EditProfile.html', context)


def register(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'grumblr/register.html', context)

    errors = []
    context['errors'] = errors
    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        context['username'] = request.POST['username']

    if not 'firstname' in request.POST or not request.POST['firstname']:
        errors.append('First Name is required.')
    else:
        context['firstname'] = request.POST['firstname']

    if not 'lastname' in request.POST or not request.POST['lastname']:
        errors.append('Last Name is required.')
    else:
        context['lastname'] = request.POST['lastname']

    if not 'email' in request.POST or not request.POST['email']:
        errors.append('Email is required.')
    else:
        context['email'] = request.POST['email']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
            and request.POST['password1'] and request.POST['password2'] \
            and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if len(User.objects.filter(username=request.POST['username'])) > 0:
        errors.append('The username is already taken.')

    if errors:
        return render(request, 'grumblr/register.html', context)

    new_user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password1'],
                                        first_name=request.POST['firstname'],
                                        last_name='/static/grumblr/images/people3.jpeg',
                                        email=request.POST['email'])
    new_user.save()
    newUser = UserProfile.objects.create(user=new_user, photopath=request.POST['lastname'])
    newUser.save()
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'])
    login(request, new_user)
    return redirect('/')
