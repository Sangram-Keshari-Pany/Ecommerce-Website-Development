# Generated by Django 5.0.6 on 2024-08-08 04:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0021_orderitems_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='order',
        ),
        migrations.AddField(
            model_name='orderitems',
            name='shiping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerceapp.shippingaddress'),
        ),
    ]
