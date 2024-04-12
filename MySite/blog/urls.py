from django.urls import path
from . import views

urlpatterns = [
    path('', views.TimeLine, name='timeline'),
    path('singup/', views.SignUp, name='sing-up-page'),
    path('login/', views.Login, name='login-page'),
]
