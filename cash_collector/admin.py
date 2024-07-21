from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Customer, Manager, CashCollector, Task


class CustomerAdmin(ModelAdmin):
    list_display = ["name", "email", "phone_number", "address"]
    search_fields = ["name", "email", "phone_number"]


class ManagerAdmin(ModelAdmin):
    list_display = ["full_name", "email", "phone_number", "address"]
    search_fields = ["user__username", "user__email", "phone_number"]
    

class CashCollectorAdmin(ModelAdmin):
    list_display = ["full_name", "email", "phone_number", "address", "status"]
    search_fields = ["user__username", "user__email", "phone_number"]
    list_filter = ["status"]


class TaskAdmin(ModelAdmin):
    list_display = ["manager", "cash_collector", "customer", "status"]
    search_fields = ["manager__user__username", "cash_collector__user__username", "customer__name"]
    list_filter = ["status"]



admin.site.register(Customer, CustomerAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(CashCollector, CashCollectorAdmin)
admin.site.register(Task, TaskAdmin)
