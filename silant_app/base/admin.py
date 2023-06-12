from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .models import UserProfile


class SpravochnikManager(admin.ModelAdmin):
    list_display = ('type_name', 'name',)
    list_filter = ('type_name',)


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


# Определяем новый класс настроек для модели User
class UserAdm(UserAdmin):
    inlines = (UserInline,)


admin.site.register(Machine)
admin.site.register(TO)
admin.site.register(Reclamation)
admin.site.register(Spravochnik, SpravochnikManager)
admin.site.unregister(User)
admin.site.register(User, UserAdm)

