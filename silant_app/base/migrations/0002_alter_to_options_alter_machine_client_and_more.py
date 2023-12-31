# Generated by Django 4.2 on 2023-04-06 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='to',
            options={'verbose_name': 'Техническое обслуживание', 'verbose_name_plural': 'Технические обслуживания'},
        ),
        migrations.AlterField(
            model_name='machine',
            name='client',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'Клиент'}, on_delete=django.db.models.deletion.CASCADE, related_name='clients', to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='drive_axle',
            field=models.ForeignKey(limit_choices_to={'type_name': 'DA'}, on_delete=django.db.models.deletion.CASCADE, related_name='drives', to='base.spravochnik', verbose_name='Модель ведущего моста'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='eng_model',
            field=models.ForeignKey(limit_choices_to={'type_name': 'EN'}, on_delete=django.db.models.deletion.CASCADE, related_name='engines', to='base.spravochnik', verbose_name='Модель двигателя'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='service',
            field=models.ForeignKey(limit_choices_to={'type_name': 'SR'}, on_delete=django.db.models.deletion.CASCADE, related_name='service_machines', to='base.spravochnik', verbose_name='Сервисная компания'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='steer_axle',
            field=models.ForeignKey(limit_choices_to={'type_name': 'SA'}, on_delete=django.db.models.deletion.CASCADE, related_name='steers', to='base.spravochnik', verbose_name='Модель управляемого моста'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='tech_model',
            field=models.ForeignKey(limit_choices_to={'type_name': 'TC'}, on_delete=django.db.models.deletion.CASCADE, related_name='techs', to='base.spravochnik', verbose_name='Модель техники'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='tran_model',
            field=models.ForeignKey(limit_choices_to={'type_name': 'TR'}, on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='base.spravochnik', verbose_name='Модель трансмиссии'),
        ),
        migrations.AlterField(
            model_name='reclamation',
            name='fail_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fails', to='base.spravochnik', verbose_name='Узел отказа'),
        ),
        migrations.AlterField(
            model_name='reclamation',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machine_reclams', to='base.machine', verbose_name='Машина'),
        ),
        migrations.AlterField(
            model_name='reclamation',
            name='recovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recovers', to='base.spravochnik', verbose_name='Способ восстановления'),
        ),
        migrations.AlterField(
            model_name='reclamation',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_reclams', to='base.spravochnik', verbose_name='Cервисная компания'),
        ),
        migrations.AlterField(
            model_name='spravochnik',
            name='type_name',
            field=models.CharField(choices=[('TC', 'Модель техники'), ('EN', 'Модель двигателя'), ('TR', 'Модель трансмиссии'), ('DA', 'Модель ведущего моста'), ('SA', 'Модель управляемого моста'), ('TO', 'Вид TO'), ('FT', 'Характер отказа'), ('RE', 'Способ восстановления'), ('SR', 'Сервисная компания')], default='Не указано', max_length=2, verbose_name='Название справочника'),
        ),
        migrations.AlterField(
            model_name='to',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machine_to', to='base.machine', verbose_name='Машина'),
        ),
        migrations.AlterField(
            model_name='to',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_to', to='base.spravochnik', verbose_name='Сервисная компания'),
        ),
        migrations.AlterField(
            model_name='to',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='base.spravochnik', verbose_name='Вид ТО'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Не указано', max_length=126, verbose_name='Описание')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
