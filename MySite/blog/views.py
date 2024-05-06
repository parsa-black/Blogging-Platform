from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
import sweetify


# Create your views here.


def TimeLine(request):
    posts = models.Post.objects.order_by('-pub_date').select_related('author').alls
    profile = None
    if request.user.is_authenticated:
        # Only get profile if the user is authenticated
        profile = get_object_or_404(models.ProfileUser, user_id=request.user.id)
    tags = models.Tag.objects.all()
    return render(request, 'TimeLine.html', {'posts': posts, 'tags': tags, 'profile': profile})


def post_single(request, post_id):
    # Get the post by ID or raise a 404 if not found
    post = get_object_or_404(models.Post, id=post_id)

    # Comments in descending order of publication
    comments = models.Comment.objects.filter(root_post=post).order_by('-pub_date')

    # Fetch the current user's profile
    profile = models.ProfileUser.objects.get(user_id=post.author.id)

    # Return the context with comments
    context = {
        'post': post,
        'comments': comments,  # Include the comments in the context
        'profile': profile,
    }

    return render(request, 'PostSingle.html', context)


def search(request):
    query = request.GET.get('query', '').strip()  # Get the search query
    profile = None
    if request.user.is_authenticated:
        # Only get profile if the user is authenticated
        profile = get_object_or_404(models.ProfileUser, user_id=request.user.id)
    txt = None  # Default message
    posts = None  # Default empty result set

    if query:
        # Check if the query matches any tag
        tags = models.Tag.objects.filter(name__iexact=query)  # Case-insensitive search for tags
        if tags.exists():
            # If a tag is found, filter posts by that tag
            tag = tags.first()  # Get the first matching tag
            posts = models.Post.objects.filter(tags=tag).distinct()
            txt = f"Posts with the tag: {query}"
        else:
            # Otherwise, perform a general search on title, content, or author username
            posts = models.Post.objects.select_related('author').filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__user__username__icontains=query)
            ).distinct()
            txt = f"Results for: {query}"

        # If no results found, set the message to indicate that
        if not posts.exists():
            txt = f"No posts found for '{query}'"

    else:
        txt = "Please enter a search query."  # No query provided

    context = {'posts': posts, 'query': query, 'txt': txt, 'profile': profile}
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
    # Get the post by ID
    post = get_object_or_404(models.Post, id=post_id)

    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)  # Instantiate form with POST data
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user.profileuser  # Set the comment author
            new_comment.root_post = post  # Set the root post
            new_comment.save()  # Save the new comment
            return redirect('post-single', post_id=post_id)

    # If not a POST request or form not valid, return an error response
    return JsonResponse({'error': 'Invalid request or form data'}, status=400)


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


def logout_view(request):
    logout(request)
    return redirect('login-page')


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

    # Post Count
    post_count = posts.count()

    return render(request, 'ProfilePage.html',
                  {
                      'posts': posts,
                      'author': profile_user,
                      'post_count': post_count,
                  })
