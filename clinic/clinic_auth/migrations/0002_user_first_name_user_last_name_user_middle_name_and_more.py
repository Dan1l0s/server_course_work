# Generated by Django 5.0 on 2023-12-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='middle_name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
