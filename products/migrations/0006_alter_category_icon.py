# Generated by Django 5.2 on 2025-06-28 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.URLField(blank=True, null=True),
        ),
    ]
