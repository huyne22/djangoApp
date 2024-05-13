# Generated by Django 4.2.11 on 2024-05-11 09:16

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_rename_shipper_order_shipper_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='order',
            new_name='order_id',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='shipper',
            new_name='shipper_id',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='shipper',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='bidder',
        ),
        migrations.AddField(
            model_name='auction',
            name='shipper_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='myapp.shipper'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shipper',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255, verbose_name='avatar'),
        ),
    ]