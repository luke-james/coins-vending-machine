from django.contrib import admin
from django.contrib.auth.models import Group

from app.models import Machine, Wallet


class WalletInline(admin.TabularInline):
    def has_add_permission(self, request):
        return False

    model = Wallet
    readonly_fields = ['units']
    can_delete = False
    extra = 0


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "token", "token_updated_at")
    search_fields = ["name"]
    empty_value_display = "-empty-"
    readonly_field = ["id"]
    inlines = [WalletInline]


admin.site.site_header = "The Vending Machine: Admin site"

# Unregister the Group model from admin.
admin.site.unregister(Group)
