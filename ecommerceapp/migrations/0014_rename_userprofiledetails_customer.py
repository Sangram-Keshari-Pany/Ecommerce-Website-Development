# Generated by Django 5.0.6 on 2024-08-07 09:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0013_alter_userprofiledetails_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfileDetails',
            new_name='Customer',
        ),
    ]
