# Generated by Django 3.2 on 2021-04-29 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_alter_article_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
