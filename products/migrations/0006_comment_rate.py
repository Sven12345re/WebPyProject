# Generated by Django 3.0.5 on 2020-07-02 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rate',
            field=models.FloatField(default=0),
        ),
    ]
