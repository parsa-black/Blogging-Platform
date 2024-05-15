from django.contrib import admin
from django.db.models import Count
from . import models
# Register your models here.


@admin.register(models.ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'post_count', 'phone_number']
    search_fields = ['get_username']
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(post_count=Count('post'))

    @admin.display(ordering='post_count')
    def post_count(self, obj):
        return obj.post_count


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_count']
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(post_count=Count('post'))

    @admin.display(ordering='post_count')
    def post_count(self, obj):
        return obj.post_count


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'pub_date']
    search_fields = ['title', 'author']
    list_per_page = 10


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'root_post']
    search_fields = ['author', 'root_post']
    list_per_page = 20
