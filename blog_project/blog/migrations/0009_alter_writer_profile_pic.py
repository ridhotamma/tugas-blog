# Generated by Django 3.2.9 on 2021-11-24 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20211123_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='avatar.png', null=True, upload_to=''),
        ),
    ]
