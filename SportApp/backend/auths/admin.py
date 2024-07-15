from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'gender',
                    'is_active', 'is_staff', 'is_superuser',
                    'datetime_created', 'datetime_updated', 'datetime_deleted')
    list_filter = ('is_active', 'is_staff', 'is_superuser',
                   'gender', 'datetime_created')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'datetime_created',
                'datetime_updated', 'datetime_deleted')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name', 'gender')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Время изменения', {'fields': ('datetime_created',
                                        'datetime_updated', 'datetime_deleted')})
    )

    add_fieldsets = (
        ('Данные для входа', {
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Личные данные', {
            'fields': ('first_name', 'last_name', 'gender', 'is_active'),
        }),
    )

    readonly_fields = ('datetime_updated',)
