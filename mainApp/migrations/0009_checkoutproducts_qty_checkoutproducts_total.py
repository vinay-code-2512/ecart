# Generated by Django 5.1.7 on 2025-03-18 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_checkout_checkoutproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutproducts',
            name='qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='checkoutproducts',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
