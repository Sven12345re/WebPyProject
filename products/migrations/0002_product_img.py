# Generated by Django 3.0.5 on 2020-06-29 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Img',
            field=models.ImageField(default=1, upload_to='products/'),
            preserve_default=False,
        ),
    ]
