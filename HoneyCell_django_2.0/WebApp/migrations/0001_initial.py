# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-21 21:20
from __future__ import unicode_literals

import WebApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=1000)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_name', models.CharField(max_length=100)),
                ('folder_time_created', models.DateTimeField(auto_now_add=True)),
                ('folder_time_changed', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Followship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_datetime', models.DateTimeField(auto_now=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_is_followed', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_follows', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pending2CompletedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True, max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('phone', models.CharField(max_length=100)),
                ('short_introduction', models.TextField(blank=True, max_length=1000)),
                ('image', models.ImageField(blank=True, upload_to=WebApp.models.generate_url_images)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_changed', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=100)),
                ('task_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('task_label', models.IntegerField(choices=[(1, 'None'), (2, 'Important'), (3, 'Warning'), (4, 'Information')], default=1)),
                ('task_status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Completed'), (3, 'Denied')], default=1)),
                ('task_algorithm', models.IntegerField(choices=[(1, 'RandomForest'), (2, 'LogisticRegression')], default=1)),
                ('training_docfile', models.FileField(upload_to=WebApp.models.generate_training_filename)),
                ('testing_docfile', models.FileField(upload_to=WebApp.models.generate_testing_filename)),
                ('task_time_created', models.DateTimeField(auto_now_add=True)),
                ('task_time_changed', models.DateTimeField(auto_now=True)),
                ('input_file_address', models.CharField(default='', max_length=100)),
                ('output_file_address', models.CharField(default='', max_length=100)),
                ('task_folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Folder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='pending2completedtask',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='WebApp.Task'),
        ),
        migrations.AddField(
            model_name='pending2completedtask',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='task',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='WebApp.Task'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
