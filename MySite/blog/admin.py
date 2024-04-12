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
