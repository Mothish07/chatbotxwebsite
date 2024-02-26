# Generated by Django 4.2.9 on 2024-02-24 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainPage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatmessage',
            old_name='content',
            new_name='input',
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='reply',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]