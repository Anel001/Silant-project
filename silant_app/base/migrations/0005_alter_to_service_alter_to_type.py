# Generated by Django 4.2 on 2023-04-07 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_machine_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='to',
            name='service',
            field=models.ForeignKey(default='самостоятельно', limit_choices_to={'type_name': 'SR'}, on_delete=django.db.models.deletion.CASCADE, related_name='service_to', to='base.spravochnik', verbose_name='Сервисная компания'),
        ),
        migrations.AlterField(
            model_name='to',
            name='type',
            field=models.ForeignKey(limit_choices_to={'type_name': 'TO'}, on_delete=django.db.models.deletion.CASCADE, related_name='types', to='base.spravochnik', verbose_name='Вид ТО'),
        ),
    ]
