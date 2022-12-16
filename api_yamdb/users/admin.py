from django.contrib import admin
from .models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )


admin.site.register(User, UserAdmin)
