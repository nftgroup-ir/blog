# Generated by Django 3.2.4 on 2021-07-12 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_alter_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
