# Generated by Django 2.2.24 on 2021-06-18 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20210611_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecogData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]