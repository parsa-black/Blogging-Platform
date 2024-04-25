from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
# from django.core.validators import MaxValueValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)


class ProfileUser(models.Model):
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True,
                                    validators=[
                                        MinLengthValidator(limit_value=10),
                                        MaxLengthValidator(limit_value=10),
                                    ])  # 0(912 345 6789)
    image = models.ImageField(upload_to='blog/media/images', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name

    def get_username(self):
        return self.user.username

    def get_password(self):
        return self.user.password

    def get_email(self):
        return self.user.email

    class Meta:
        verbose_name = 'User'


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=25)
    content = RichTextUploadingField()
    pub_date = models.DateTimeField(auto_now_add=True)
    root_post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='blog/media/images', null=True, blank=True)

    def __str__(self):
        return self.title
