# Generated by Django 5.0.6 on 2024-08-08 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0025_product_serching'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='serching',
            new_name='serchingitems',
        ),
    ]
