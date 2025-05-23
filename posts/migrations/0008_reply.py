# Generated by Django 5.2 on 2025-05-13 14:19

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('body', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to=settings.AUTH_USER_MODEL)),
                ('parent_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='posts.comment')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
