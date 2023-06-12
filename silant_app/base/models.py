from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions.datetime import ExtractDay


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',)
    name = models.CharField(max_length=126,  verbose_name='Описание')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Machine(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name='Зав. № машины')
    tech_model = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                   related_name='techs',
                                   limit_choices_to={'type_name': 'TC'},
                                   verbose_name='Модель техники')
    eng_model = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                  related_name='engines',
                                  limit_choices_to={'type_name': 'EN'},
                                  verbose_name='Модель двигателя')
    eng_num = models.CharField(max_length=50, unique=True, verbose_name='Зав. № двигателя')
    tran_model = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                   related_name='trans',
                                   limit_choices_to={'type_name': 'TR'},
                                   verbose_name='Модель трансмиссии')
    tran_num = models.CharField(max_length=50, unique=True, verbose_name='Зав. № трансмиссии')
    drive_axle = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                   related_name='drives',
                                   limit_choices_to={'type_name': 'DA'},
                                   verbose_name='Модель ведущего моста')
    drive_num = models.CharField(max_length=50, unique=True, verbose_name='Зав. № ведущего моста')
    steer_axle = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                   related_name='steers',
                                   limit_choices_to={'type_name': 'SA'},
                                   verbose_name='Модель управляемого моста')
    steer_num = models.CharField(max_length=50, unique=True, verbose_name='Зав. № управляемого моста')
    dogovor = models.CharField(max_length=126, verbose_name='Договор поставки №, дата')
    shipping_date = models.DateField(verbose_name='Дата отгрузки с завода')
    consumer = models.CharField(max_length=126, verbose_name='Грузополучатель (конечный потребитель)')
    address = models.CharField(max_length=126, verbose_name='Адрес поставки (эксплуатации)')
    package = models.TextField(default="Стандарт", verbose_name='Комплектация (доп. опции)')
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                               related_name='clients',
                               limit_choices_to={'user__groups__name': 'Клиент'},
                               verbose_name='Клиент')
    service = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                related_name='service_machines',
                                limit_choices_to={'type_name': 'SR'},
                                verbose_name='Сервисная компания')

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return 'Номер машины: {}'.format(self.number)


class TO(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE,
                                related_name='machine_to',
                                verbose_name='Машина')
    type = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                             related_name='types',
                             limit_choices_to={'type_name': 'TO'},
                             verbose_name='Вид ТО')
    to_date = models.DateField(verbose_name='Дата проведения ТО')
    operating = models.IntegerField(default=0, verbose_name='Наработка, м/час')
    order_num = models.CharField(max_length=50, verbose_name='№ заказ-наряда')
    order_date = models.DateField(verbose_name='Дата заказ-наряда')
    service = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                related_name='service_to',
                                limit_choices_to={'type_name': 'SR'},
                                verbose_name='Сервисная компания')

    class Meta:
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Технические обслуживания'

    def __str__(self):
        return 'Заказ-наряд: {}'.format(self.order_num)


class Reclamation(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE,
                                related_name='machine_reclams',
                                verbose_name='Машина')
    fail_date = models.DateField(verbose_name='Дата отказа')
    operating = models.IntegerField(default=0, verbose_name='Наработка, м/час')
    fail_node = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                  related_name='fails',
                                  limit_choices_to={'type_name': 'FT'},
                                  verbose_name='Узел отказа')
    fail_descrip = models.CharField(max_length=126, verbose_name='Описание отказа')
    recovery = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                 related_name='recovers',
                                 limit_choices_to={'type_name': 'RE'},
                                 verbose_name='Способ восстановления')
    parts = models.CharField(max_length=126, verbose_name='Используемые запасные части')
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    idleness = models.IntegerField(default=0, verbose_name='Время простоя техники')
    service = models.ForeignKey('Spravochnik', on_delete=models.CASCADE,
                                related_name='service_reclams',
                                limit_choices_to={'type_name': 'SR'},
                                verbose_name='Cервисная компания')

    def __str__(self):
        return '{} с отказом: {}'.format(self.machine, self.fail_descrip)

    """Функция, вызываемая в сигнале post_save: расчет количества дней"""
    def duration(self):
        days = (self.recovery_date - self.fail_date).days
        return days

    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'


class Spravochnik(models.Model):
    TECHNIQUE = 'TC'
    ENGINE = 'EN'
    TRANSMISSION = 'TR'
    DRIVE_AXLE = 'DA'
    STEERING_AXLE = 'SA'
    TO_TYPE = 'TO'
    FAILURE = 'FT'
    RECOVERY = 'RE'
    SERVICE = 'SR'
    HANDBOOK_CHOICES = [
        (TECHNIQUE, 'Модель техники'),
        (ENGINE, 'Модель двигателя'),
        (TRANSMISSION, 'Модель трансмиссии'),
        (DRIVE_AXLE, 'Модель ведущего моста'),
        (STEERING_AXLE, 'Модель управляемого моста'),
        (TO_TYPE, 'Вид TO'),
        (FAILURE, 'Характер отказа'),
        (RECOVERY, 'Способ восстановления'),
        (SERVICE, 'Сервисная компания'),
    ]
    type_name = models.CharField(
        max_length=2,
        choices=HANDBOOK_CHOICES,
        default='Не указано',
        verbose_name='Название справочника'
    )
    name = models.CharField(max_length=256, db_index=True, verbose_name='Название')
    description = models.CharField(max_length=2000, default='Отсутствует', verbose_name='Описание')

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self):
        return self.name

# Create your models here.
