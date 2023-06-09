# Generated by Django 3.2.2 on 2023-03-18 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_auto_20230316_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='company',
            field=models.CharField(max_length=150, null=True, verbose_name='Company name'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='measurement',
            field=models.CharField(blank=True, choices=[('kilos', 'kilos'), ('grams', 'grams'), ('kilograms', 'kilograms'), ('pieces', 'pieces'), ('crates', 'crates'), ('rolls', 'rolls'), ('cups', 'cups'), ('paints', 'paints'), ('sacks', 'sacks'), ('bags', 'bags'), ('package', 'package'), ('baskets', 'baskets'), ('buckets', 'buckets'), ('trucks', 'trucks')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='shippingdetail',
            name='phone1',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Land phone number'),
        ),
        migrations.AlterField(
            model_name='shippingdetail',
            name='phone2',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Mobile phone number'),
        ),
    ]
