# Generated by Django 4.2 on 2023-04-07 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_machine_client_alter_machine_shipping_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='package',
            field=models.TextField(default='Стандарт', verbose_name='Комплектация (доп. опции)'),
        ),
    ]
