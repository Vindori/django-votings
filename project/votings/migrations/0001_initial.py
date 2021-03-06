# Generated by Django 3.0.2 on 2020-01-24 12:08

import datetime
from django.db import migrations, models
import django.db.models.deletion
import votings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('topic', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('cr_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='creation date')),
                ('public', models.BooleanField(default=True)),
                ('access_token', models.CharField(default=votings.models.random_token, max_length=16, primary_key=True, serialize=False, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votings.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votings.Question')),
            ],
        ),
    ]
