# Generated by Django 4.2.11 on 2024-05-12 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_rename_order_id_auction_order_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='user_id',
        ),
    ]