from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reclamation

""" Вычисляемое поле idleness модели Reclamation """
@receiver(post_save, sender=Reclamation)
def my_callback(sender, instance, *args, **kwargs):
    idleness = instance.duration()
    sender.objects.filter(pk=instance.pk).update(idleness=idleness)


