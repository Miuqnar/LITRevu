# Generated by Django 5.0.4 on 2024-04-18 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('litrevu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, max_length=8192),
        ),
    ]
