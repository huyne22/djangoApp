# Generated by Django 4.2.11 on 2024-04-03 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_user_cccd_user_is_shipper_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
