# Generated by Django 2.2.3 on 2020-09-15 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200915_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='Shirt'),
            preserve_default=False,
        ),
    ]
