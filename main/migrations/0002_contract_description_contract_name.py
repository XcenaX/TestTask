# Generated by Django 4.2.1 on 2024-05-09 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='contract',
            name='name',
            field=models.TextField(default='Контракт'),
        ),
    ]
