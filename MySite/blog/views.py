from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
import sweetify

# Create your views here.


def post_single(request, post_id):
    post = models.Post.objects.get(id=post_id)
    return render(request, 'PostSingle.html', context={'post': post})


@login_required()
def create_post(request):
    if not request.user.is_staff:
        if request.method == "POST":
            post_form = forms.PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post_instance = post_form.save(commit=False)
                post_form.instance.author = request.user.profileuser
                post_form.save()
                return redirect('timeline')
        else:
            post_form = forms.PostForm()

        return render(request, 'NewPost.html', {'post_form': post_form})
    else:
        sweetify.error(request, 'Access Denied')
        return redirect('timeline')


def TimeLine(request):
    posts = models.Post.objects.order_by('-pub_date').all
    tags = models.Tag.objects.all()
    return render(request, 'TimeLine.html', {'posts': posts, 'tags': tags})


def SignUp(request):
    sign_msg = None
    user_form = forms.UserForm(request.POST)
    profile_form = forms.ProfileForm(request.POST, request.FILES)

    if request.method == 'POST':
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
                return redirect('timeline')
            else:
                sign_msg = 'Password should be equal to password confirm'
    else:
        user_form = forms.UserForm()
        profile_form = forms.ProfileForm()
    return render(request, 'SingUp.html', {
        'UserForm': user_form,
        'ProfileForm': profile_form,
        'sign_msg': sign_msg
    })


def Login(request):
    login_msg = None
    loginform = forms.LoginForm(request.POST or None)

    if request.method == 'POST':
        if loginform.is_valid():
            username = loginform.cleaned_data.get('username')
            password = loginform.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('timeline')
            else:
                login_msg = 'Invalid credentials'
        else:
            login_msg = 'Error validating the form'

    return render(request, 'Login.html', {'LoginForm': loginform, 'login_msg': login_msg})
