# Generated by Django 4.1.1 on 2022-10-03 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_rename_song_somethingelse'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SomethingElse',
            new_name='Song',
        ),
    ]
