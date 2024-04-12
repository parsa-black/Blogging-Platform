from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

# Create your views here.


def Timeline(request):
    posts = models.Post.objects.all
    return render(request, 'TimeLine.html', {'posts': posts})


def SignUp(request):
    msg = None
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST)
        profile_form = forms.ProfileForm(request.POST, request.FILES)
        if user_form.is_valid():
            if user_form.cleaned_data.get('password') == user_form.cleaned_data.get('confirm_password'):
                user = user_form.save(commit=False)
                hashed_password = make_password(user_form.cleaned_data['password'])
                # Create a user object but don't save
                user.password = hashed_password
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user  # Associate the profile with the user
                profile.save()
                return redirect('login-page')
            else:
                msg = 'Password should be equal to password confirm'
    else:
        user_form = forms.UserForm()
        profile_form = forms.ProfileForm()
    return render(request, 'SingUp.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'msg': msg
    })


def Login(request):
    if request.user.is_authenticated:
        return redirect('home-page')

    form = forms.LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home-page')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, 'Login.html', {'form': form, 'msg': msg})
