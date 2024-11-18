# Generated by Django 5.0rc1 on 2024-10-13 19:23

import notes.helpers.model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_alter_note_options_remove_note_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(to='notes.tag'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(upload_to=notes.helpers.model.PathAndRename.wrapper),
        ),
    ]