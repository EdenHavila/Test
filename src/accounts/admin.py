from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role
# Register your models here.


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('nom_role',)

class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'role', 'statut_utilisateur', 'date_creation_utilisateur', 'is_staff'
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'statut_utilisateur', 'date_creation_utilisateur')
        }),
    )

admin.site.register(User, CustomUserAdmin)
