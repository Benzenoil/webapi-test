# Generated by Django 2.1.7 on 2019-04-01 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0005_auto_20190401_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='signup',
            name='nick_name',
            field=models.TextField(null=True),
        ),
    ]
