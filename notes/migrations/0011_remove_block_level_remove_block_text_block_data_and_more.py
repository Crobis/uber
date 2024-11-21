# Generated by Django 5.0rc1 on 2024-11-21 15:12

import notes.helpers.model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0010_picture_type_alter_picture_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='level',
        ),
        migrations.RemoveField(
            model_name='block',
            name='text',
        ),
        migrations.AddField(
            model_name='block',
            name='data',
            field=models.JSONField(blank=True, null=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='block',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='block',
            name='type',
            field=models.CharField(choices=[('header', 'Header'), ('paragraph', 'Paragraph'), ('linktool', 'LinkTool')], max_length=20),
        ),
        migrations.AlterField(
            model_name='picture',
            name='pic',
            field=models.ImageField(upload_to=notes.helpers.model.PathAndRename.wrapper),
        ),
    ]