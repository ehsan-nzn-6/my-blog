# Generated by Django 3.1.7 on 2021-03-29 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import extensions.jalaliconverter


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DakhlOKharj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('date', models.CharField(blank=True, default=extensions.jalaliconverter.mydate, max_length=50, null=True)),
                ('amount', models.FloatField()),
                ('kharj', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
