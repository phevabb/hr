from django.contrib import admin

from .models import ManagerProfile
from django.contrib.auth import get_user_model
User = get_user_model()

# Register your models here.
@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'region')
    # Optional: filter only Manager users in admin dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="Manager")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
