from django import forms
from . import models


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        max_length= 20,
        widget=forms.TextInput(attrs={'placeholder': 'FirstName'}),
        error_messages={'required': 'Please Fill The Filed',
                        'max_length': 'Maximum Length is 20'}
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'LastName'}),
        error_messages={'required': 'Please Fill The Filed',
                        'max_length': 'Maximum Length is 20'}
    )

    username = forms.CharField(
        label='Username',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        error_messages={'required': 'Please Fill The Filed',
                        'max_length': 'Maximum Length is 20'}
    )

    password = forms.CharField(
        label='Password',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Password'}),
        error_messages={'required': 'Please Fill The Filed',
                        'max_length': 'Maximum Length is 30'}
    )

    email = forms.EmailField(
        label='Email',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        error_messages={'required': 'Please Fill The Filed',
                        'max_length': 'Maximum Length is 50'}
    )

    confirm_password = password = forms.CharField(
        label='Confirm Password',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Confirm Password'}),
        error_messages={'required': 'Please Enter Your Password',
                        'max_length': 'Password Max Length Must Be 30 Characters'}
    )

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'confirm_password']
