# Generated by Django 4.2.11 on 2024-05-12 09:50

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_rename_shipper_id_order_shipper_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='bid_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='auction',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.order'),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default='', max_length=255, verbose_name='avatar'),
        ),
    ]
