# Generated by Django 4.2 on 2023-04-06 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, unique=True, verbose_name='Зав. № машины')),
                ('eng_num', models.CharField(max_length=50, verbose_name='Зав. № двигателя')),
                ('tran_num', models.CharField(max_length=50, verbose_name='Зав. № трансмиссии')),
                ('drive_num', models.CharField(max_length=50, verbose_name='Зав. № ведущего моста')),
                ('steer_num', models.CharField(max_length=50, verbose_name='Зав. № управляемого моста')),
                ('dogovor', models.CharField(max_length=126, verbose_name='Договор поставки №, дата')),
                ('shipping_date', models.DateField(auto_now_add=True, verbose_name='Дата отгрузки с завода')),
                ('consumer', models.CharField(max_length=126, verbose_name='Грузополучатель (конечный потребитель)')),
                ('address', models.CharField(max_length=126, verbose_name='Адрес поставки (эксплуатации)')),
                ('package', models.TextField(default='Не имеются', verbose_name='Комплектация (доп. опции)')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Машина',
                'verbose_name_plural': 'Машины',
            },
        ),
        migrations.CreateModel(
            name='Spravochnik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(choices=[('TC', 'Модель техники'), ('EN', 'Модель двигателя'), ('TR', 'Модель трансмиссии'), ('DA', 'Модель ведущего моста'), ('SA', 'Модель управляемого моста'), ('TO', 'Вид TO'), ('FT', 'Характер отказа'), ('RE', 'Способ восстановления'), ('RE', 'Сервисная компания')], default='Не указано', max_length=2, verbose_name='Название справочника')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Название')),
                ('description', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
            },
        ),
        migrations.CreateModel(
            name='TO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_date', models.DateField(auto_now_add=True, verbose_name='Дата проведения ТО')),
                ('operating', models.IntegerField(default=0, verbose_name='Наработка, м/час')),
                ('order_num', models.CharField(max_length=50, verbose_name='№ заказ-наряда')),
                ('order_date', models.DateField(auto_now_add=True, verbose_name='Дата заказ-наряда')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machine_to', to='base.machine')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_to', to='base.spravochnik')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='base.spravochnik')),
            ],
            options={
                'verbose_name': 'Техническое обслуживание',
            },
        ),
        migrations.CreateModel(
            name='Reclamation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fail_date', models.DateField(auto_now_add=True, verbose_name='Дата отказа')),
                ('operating', models.IntegerField(default=0, verbose_name='Наработка, м/час')),
                ('fail_descrip', models.CharField(max_length=126, verbose_name='Описание отказа')),
                ('parts', models.CharField(max_length=126, verbose_name='Используемые запасные части')),
                ('recovery_date', models.DateField(auto_now_add=True, verbose_name='Дата восстановления')),
                ('idleness', models.IntegerField(default=0, verbose_name='Время простоя техники')),
                ('fail_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fails', to='base.spravochnik')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machine_reclams', to='base.machine')),
                ('recovery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recovers', to='base.spravochnik')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_reclams', to='base.spravochnik')),
            ],
            options={
                'verbose_name': 'Рекламация',
                'verbose_name_plural': 'Рекламации',
            },
        ),
        migrations.AddField(
            model_name='machine',
            name='drive_axle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drives', to='base.spravochnik'),
        ),
        migrations.AddField(
            model_name='machine',
            name='eng_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engines', to='base.spravochnik'),
        ),
        migrations.AddField(
            model_name='machine',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_machines', to='base.spravochnik'),
        ),
        migrations.AddField(
            model_name='machine',
            name='steer_axle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steers', to='base.spravochnik'),
        ),
        migrations.AddField(
            model_name='machine',
            name='tech_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='techs', to='base.spravochnik'),
        ),
        migrations.AddField(
            model_name='machine',
            name='tran_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='base.spravochnik'),
        ),
    ]
