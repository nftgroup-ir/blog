# Generated by Django 3.2.5 on 2021-08-09 06:49

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0019_auto_20210731_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
