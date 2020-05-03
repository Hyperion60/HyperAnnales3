from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'is_contributor', 'is_active',)
    search_fields = ('email', 'username', 'date_joined', 'is_active')
    readonly_fields = ('date_joined', 'last_login',)
    ordering = ('username',)

    filter_horizontal = ()
    list_filter = ('is_active',)
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
