from django.urls import path
from . import views

urlpatterns = [
    path('', views.TimeLine, name='timeline'),
    path('singup/', views.SignUp, name='sing-up-page'),
    path('login', views.Login, name='login-page'),
    path('create', views.create_post, name='create-post'),
    path('search/', views.search, name='search-page'),
    path('post/<int:post_id>', views.post_single, name='post-single'),
    path('comment/<int:post_id>/', views.create_comment, name='create-comment'),
    path('profile/<str:username>', views.profile_view, name='profile-page')
]
