# Generated by Django 3.2.15 on 2022-08-14 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_devicedata_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicedata',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='devicedata',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]