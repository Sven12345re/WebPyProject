# Generated by Django 3.0.7 on 2020-07-10 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200710_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='commnet',
            new_name='comment',
        ),
    ]
