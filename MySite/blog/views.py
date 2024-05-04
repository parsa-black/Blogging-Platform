from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
import sweetify

# Create your views here.


def TimeLine(request):
    posts = models.Post.objects.order_by('-pub_date').select_related('author').all
    profile = models.ProfileUser.objects.get(user_id=request.user.id)
    tags = models.Tag.objects.all()
    return render(request, 'TimeLine.html', {'posts': posts, 'tags': tags, 'profile': profile})


def post_single(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    profile = models.ProfileUser.objects.get(user_id=request.user.id)
    return render(request, 'PostSingle.html', context={'post': post, 'profile': profile})


def search(request):
    query = request.GET.get('query')
    txt = None
    posts = None
    if query:
        posts = models.Post.objects.select_related('author').filter(Q(title__icontains=query) |
                                                                    Q(content__icontains=query)
                                                                    | Q(tags__name__icontains=query) |
                                                                    Q(author__user__username__icontains=query))
        context = {'posts': posts, 'query': query, 'txt': txt}
        return render(request, 'TimeLine.html', context)
    else:
        txt = 'No posts found'

    context = {'posts': posts, 'query': query, 'txt': txt}
    return render(request, 'TimeLine.html', context)


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


@login_required
def create_comment(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)  # Ensures post exists
    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user.profileuser
            new_comment.root_post = post
            new_comment.save()  # Save the comment
            return redirect('post-single', post_id=post_id)  # Redirects to the post
    else:
        comment_form = forms.CommentForm()  # Initialize empty form

    return render(request, 'NewComment.html', {
        'comment_form': comment_form,
        'post': post,
    })


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


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(models.User, username=username)
    follow, created = models.Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    if created:
        return JsonResponse({'message': f'Now following {username}'})
    else:
        return JsonResponse({'message': f'Already following {username}'})


@login_required
@transaction.atomic
def unfollow_user(request, username):
    # Find the user to unfollow
    user_to_unfollow = get_object_or_404(models.User, username=username)

    # Get the follow object that represents the relationship
    follow = models.Follow.objects.filter(follower=request.user, followed=user_to_unfollow)

    if follow.exists():
        follow.delete()  # Delete the relationship
        return JsonResponse({'message': f'Successfully unfollowed {username}'})

    # If there is no relationship, return an appropriate message
    return JsonResponse({'message': f'You were not following {username}'})


def profile_view(request, username):
    # Fetch the related User instance by username
    user_instance = get_object_or_404(models.User, username=username)

    # Fetch the ProfileUser related to the User instance
    profile_user = get_object_or_404(models.ProfileUser, user=user_instance)

    # Fetch all posts authored by this ProfileUser
    posts = models.Post.objects.filter(author=profile_user).order_by('-pub_date')

    return render(request, 'ProfilePage.html', {'posts': posts, 'author': profile_user})
