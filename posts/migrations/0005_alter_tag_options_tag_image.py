# Generated by Django 5.2 on 2025-05-07 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_tag_options_tag_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-order']},
        ),
        migrations.AddField(
            model_name='tag',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='icons/'),
        ),
    ]
