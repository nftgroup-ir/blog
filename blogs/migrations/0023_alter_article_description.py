# Generated by Django 3.2.5 on 2021-08-11 10:04

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0022_alter_article_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]