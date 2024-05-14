# Generated by Django 5.0.4 on 2024-05-14 02:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_remove_comment_image_remove_comment_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='arent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
