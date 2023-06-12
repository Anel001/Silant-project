# Generated by Django 4.2 on 2023-04-07 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_to_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamation',
            name='fail_node',
            field=models.ForeignKey(limit_choices_to={'type_name': 'FT'}, on_delete=django.db.models.deletion.CASCADE, related_name='fails', to='base.spravochnik', verbose_name='Узел отказа'),
        ),
    ]