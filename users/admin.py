from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'is_superuser', 'is_staff', 'is_active', 'role')
    readonly_fields = ["email"]
    model = User


admin.site.register(User, UserAdmin)
