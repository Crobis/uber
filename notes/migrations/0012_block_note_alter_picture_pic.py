# Generated by Django 5.0rc1 on 2024-11-21 15:13

import django.db.models.deletion
import notes.helpers.model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0011_remove_block_level_remove_block_text_block_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='note',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='notes.note'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(upload_to=notes.helpers.model.PathAndRename.wrapper),
        ),
    ]