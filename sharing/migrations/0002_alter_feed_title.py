# Generated by Django 3.2.9 on 2021-12-22 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='Title',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
