from django.contrib import admin

from users.models import User


@admin.register(User)
class Administrator(admin.ModelAdmin):
    list_display = ('email',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Administrator').exists():
            return ['email', 'avatar', 'phone', 'country', 'rand_key', 'first_name', 'last_name', 'is_staff',
                    'date_joined', 'is_superuser', 'password', 'groups', 'user_permissions', 'last_login']
        return []
