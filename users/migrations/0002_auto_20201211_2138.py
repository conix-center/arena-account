# Generated by Django 3.0.7 on 2020-12-11 21:38

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scene',
            name='title',
        ),
        migrations.AddField(
            model_name='scene',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scene',
            name='editors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scene',
            name='name',
            field=models.CharField(default='scene', max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scene',
            name='public_read',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='scene',
            name='public_write',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='scene',
            name='summary',
            field=models.TextField(max_length=1000),
        ),
    ]
