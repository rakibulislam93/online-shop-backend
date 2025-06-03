from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ['username','id','email','user_role','is_active','approval_status']

    fieldsets = UserAdmin.fieldsets +(
        ('Extra Info',{'fields':('user_role','approval_status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets +(
        ('Extra Info',{'fields':('user_role','approval_status')}),
    )

admin.site.register(models.CustomUser,CustomUserAdmin)
admin.site.register(models.Profile)
