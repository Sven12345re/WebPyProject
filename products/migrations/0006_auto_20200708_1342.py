# Generated by Django 3.0.5 on 2020-07-08 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200708_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='report',
            field=models.FloatField(max_length=500, null=True),
        ),
    ]
