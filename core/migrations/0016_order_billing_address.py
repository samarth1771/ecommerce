# Generated by Django 2.2.3 on 2020-09-16 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_billingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.BillingAddress'),
        ),
    ]
