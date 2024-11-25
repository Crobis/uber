# Generated by Django 5.0rc1 on 2024-04-05 08:57

import django.db.models.deletion
import notes.helpers.model
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, verbose_name='Title')),
                ('description', models.JSONField(blank=True, null=True, verbose_name='Description')),
                ('archive', models.BooleanField(default=False, verbose_name='Archive')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Izveidots')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Labots')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_note', to=settings.AUTH_USER_MODEL, verbose_name='Lietotājs izveidoja')),
                ('user_modified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_note', to=settings.AUTH_USER_MODEL, verbose_name='Lietotājs laboja')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to=notes.helpers.model.PathAndRename.wrapper)),
                ('original_filename', models.CharField(blank=True, max_length=250, verbose_name='Original filename')),
                ('title_lv', models.CharField(blank=True, max_length=250, verbose_name='Title')),
                ('title_en', models.CharField(blank=True, max_length=250, verbose_name='Title')),
                ('description_lv', models.TextField(blank=True, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, verbose_name='Description')),
                ('object_id', models.PositiveIntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Izveidots')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Labots')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_picture', to=settings.AUTH_USER_MODEL, verbose_name='Lietotājs izveidoja')),
                ('user_modified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_picture', to=settings.AUTH_USER_MODEL, verbose_name='Lietotājs laboja')),
            ],
        ),
    ]
