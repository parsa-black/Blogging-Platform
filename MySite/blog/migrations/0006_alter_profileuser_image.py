# Generated by Django 5.0.4 on 2024-04-12 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_post_image_remove_post_is_published_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog/media/images'),
        ),
    ]
