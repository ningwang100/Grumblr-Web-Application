from django import forms
from models import *
from string import lower

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'class': 'user', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'user', 'placeholder': 'Password'}))


class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=40,
                             label='Email',
                             error_messages={'required': 'Email is required'},
                             widget=forms.EmailInput(attrs={'class': 'r1', 'placeholder': 'Valid email'}))
    first_name = forms.CharField(max_length=40,
                                 label='First Name',
                                 error_messages={'required': 'First name is required'},
                                 widget=forms.TextInput(attrs={'class': 'r1', 'placeholder': 'enter your first name'}))
    last_name = forms.CharField(max_length=40,
                                label='Last Name',
                                error_messages={'required': 'Last name is required'},
                                widget=forms.TextInput(attrs={'class': 'r1', 'placeholder': 'enter your last name'}))
    age = forms.CharField(max_length=40,
                          label='Age',
                          widget=forms.TextInput(attrs={'class': 'r1', 'placeholder': 'enter your age'}))
    username = forms.CharField(max_length=40,
                               label='Username',
                               error_messages={'required': 'Username is required'},
                               widget=forms.TextInput(attrs={'class': 'r2', 'placeholder': 'enter your username'}))
    avatar = forms.ImageField(error_messages={'required': 'Avatar is required'},
                              label='Choose your avatar',
                              widget=forms.ClearableFileInput(attrs={'class': 'r2'}))

    password1 = forms.CharField(max_length=40,
                                label='Choose a password',
                                error_messages={'required': 'Password is required'},
                                widget=forms.PasswordInput(attrs={'class': 'r2', 'placeholder': 'enter your password'}))
    password2 = forms.CharField(max_length=40,
                                label='Re_enter password',
                                error_messages={'required': 'Double check your password is required'},
                                widget=forms.PasswordInput(
                                    attrs={'class': 'r2', 'placeholder': 'enter your password again'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already registered.")
        return email


class SendEmailForm(forms.Form):
    email = forms.EmailField(max_length=100,
                             label='Email:',
                             error_messages={'required': 'Email is required'},
                             widget=forms.EmailInput(attrs={'class':'r3',
                                                            'placeholder': 'enter your email'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(User.objects.filter(email=email)) == 0:
            raise forms.ValidationError("This Email not exist .")
        return email


class resetForm(forms.Form):
    password1 = forms.CharField(max_length=40,
                                label='Choose a password',
                                error_messages={'required': 'Password is required'},
                                widget=forms.PasswordInput(attrs={'class': 'r2', 'placeholder': 'enter your password'}))
    password2 = forms.CharField(max_length=40,
                                label='Re_enter password',
                                error_messages={'required': 'Double check your password is required'},
                                widget=forms.PasswordInput(
                                    attrs={'class': 'r2', 'placeholder': 'enter your password again'}))

    def clean(self):
        cleaned_data = super(resetForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data


class PostForm(forms.Form):
    content = forms.CharField(max_length=42,
                              error_messages={'required': 'You must enter something.',
                                              'max_length': 'You post message need to 42 characters or less.'},
                              widget=forms.Textarea(attrs={'id': 'textarea1',
                                                           'placeholder': 'enter yuor post here...'}))


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=42,
                              error_messages={'required': 'You need to enter keyword.',
                                              'max_length': 'Your keyword is too long'},
                              widget=forms.TextInput(attrs={'class': 'form-control pull-right',
                                                            'placeholder': 'Search...'}))


class EditForm(forms.Form):
    first_name = forms.CharField(max_length=40,
                                 label='First Name:',
                                 required=False,
                                 error_messages={'required': 'First name is required'},
                                 widget=forms.TextInput(attrs={'class': 'r1', 'placeholder': 'enter your first name'}))
    last_name = forms.CharField(max_length=40,
                                label='Last Name:',
                                required=False,
                                error_messages={'required': 'Last name is required'},
                                widget=forms.TextInput(attrs={'class': 'r1', 'placeholder': 'enter your last name'}))
    age = forms.CharField(max_length=40,
                          label='Age:',
                          required=False,
                          widget=forms.TextInput(attrs={'class': 'r1', 'placeholder': 'change your age'}))
    email = forms.EmailField(max_length=40,
                             label='Email:',
                             required=False,
                             error_messages={'required': 'Email is required'},
                             widget=forms.EmailInput(attrs={'class': 'r1 read', 'placeholder': 'Valid email','readonly':True}))
    avatar = forms.ImageField(label="Change your avatar",
                              required=False,
                              error_messages={'required': 'Avatar is required.',
                                              'invalid': 'The avatar is invalid.'},
                              widget=forms.ClearableFileInput(attrs={'class': 'r1'}))
    oldPassword = forms.CharField(label="Old Password:",
                                  max_length=42,
                                  required=False,
                                  widget=forms.PasswordInput(
                                      attrs={'class': 'r2', 'placeholder': 'Enter old password'}))
    password1 = forms.CharField(max_length=40,
                                label='Choose a password',
                                required=False,
                                widget=forms.PasswordInput(attrs={'class': 'r2', 'placeholder': 'enter your password'}))
    password2 = forms.CharField(max_length=40,
                                label='Re_enter password',
                                required=False,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'r2', 'placeholder': 'enter your password again'}))
    self_bio = forms.CharField(label='Short bio:',
                               max_length=420,
                               required=False,
                               error_messages={'max_length': 'Your bio need to 420 characters or less'},
                               widget=forms.Textarea(
                                   attrs={'class': 'r2 textarea1', 'placeholder': 'Enter your short bio here...'}))

    def clean(self):
        cleaned_data = super(EditForm, self).clean()
        if cleaned_data.get('oldPassword'):
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')
            if not password1 or not password2:
                raise forms.ValidationError("Passwords are required.")
            if password1 != password2:
                raise forms.ValidationError("New passwords did not match.")
        elif cleaned_data.get('oldPassword') == "":
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')
            if password1 or password2:
                raise forms.ValidationError("Old password are required.")
        return cleaned_data
