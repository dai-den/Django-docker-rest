# Generated by Django 2.2.24 on 2021-06-18 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_conversationdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationdata',
            name='data',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]