# Generated by Django 4.2.6 on 2023-11-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.CharField(default='johndoe.png', max_length=255),
        ),
    ]
