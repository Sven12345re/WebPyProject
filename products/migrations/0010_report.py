# Generated by Django 3.0.5 on 2020-07-08 22:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0009_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.CharField(choices=[('R', 'REPORT')], max_length=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('commnet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]