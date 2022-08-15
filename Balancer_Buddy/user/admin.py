from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .forms import CustomUserRegistrationForm, CustomUserChangeForm
from django.contrib.auth.models import User
from .models import *

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserRegistrationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active','first_name', 'last_name',)
    list_filter = ('email', 'is_staff', 'is_active','first_name', 'last_name','groups',)
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name', 'last_name','groups',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    inlines = (ProfileInline,)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name', 'last_name','password1', 'password2', 'is_staff', 'is_active','groups',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(DeviceData)