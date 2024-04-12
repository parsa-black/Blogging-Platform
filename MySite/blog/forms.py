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


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        label='Birth Date',
        widget=forms.DateInput(attrs={'placeholder': 'BirthDate', 'type': 'date'})
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=10,
        min_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        error_messages={'required': 'Please Enter Your Phone Number',
                        'max_length': 'Phone Number must be 10 Characters',
                        'min_length': 'Phone Number must be 10 Characters'}
    )

    image = forms.ImageField(
        required=False
    )

    class Meta:
        model = models.ProfileUser
        fields = ['birth_date', 'phone_number', 'image']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

    class Meta:
        model = models.User
        fields = ['username', 'password']
