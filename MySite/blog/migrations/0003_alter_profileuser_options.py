# Generated by Django 5.0.4 on 2024-04-12 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_profileuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profileuser',
            options={'verbose_name': 'User'},
        ),
    ]