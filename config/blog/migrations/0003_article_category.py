# Generated by Django 3.2.8 on 2021-10-08 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20211008_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(to='blog.Category', verbose_name='دسته بندی'),
        ),
    ]
