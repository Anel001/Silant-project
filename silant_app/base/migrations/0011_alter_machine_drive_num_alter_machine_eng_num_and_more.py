# Generated by Django 4.2 on 2023-04-09 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='drive_num',
            field=models.CharField(max_length=50, unique=True, verbose_name='Зав. № ведущего моста'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='eng_num',
            field=models.CharField(max_length=50, unique=True, verbose_name='Зав. № двигателя'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='steer_num',
            field=models.CharField(max_length=50, unique=True, verbose_name='Зав. № управляемого моста'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='tran_num',
            field=models.CharField(max_length=50, unique=True, verbose_name='Зав. № трансмиссии'),
        ),
    ]