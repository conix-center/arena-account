# Generated by Django 3.0.7 on 2021-02-02 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201211_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scene',
            name='public_write',
            field=models.BooleanField(default=False),
        ),
    ]
