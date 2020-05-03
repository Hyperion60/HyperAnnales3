from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'is_contributor',)
    search_fields = ('email', 'username', 'date_joined',)
    readonly_fields = ('date_joined', 'last_login',)
    ordering = ('username',)

    filter_horizontal = ()
    list_filter = ('is_active', 'is_staff',)
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
