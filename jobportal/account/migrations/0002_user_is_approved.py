# Generated by Django 5.0.4 on 2024-04-25 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Is approved'),
        ),
    ]
