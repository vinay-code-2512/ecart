# Generated by Django 5.1.6 on 2025-03-11 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_brand_pic_alter_product_pic1_alter_product_pic2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('addressline1', models.CharField(max_length=100)),
                ('addressline2', models.CharField(max_length=100)),
                ('addressline3', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('pic', models.ImageField(upload_to='buyers')),
            ],
        ),
    ]
