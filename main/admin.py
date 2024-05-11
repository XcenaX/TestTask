from django.contrib import admin
from main.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    filter_horizontal = ['roles']

class ContractAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description', 'child_company__name', 'contractor__name']
    filter_horizontal = ['roles']

class ContractRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class ContractAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'contract', 'role']
    search_fields = ['user__email', 'contract__name', 'contract__child_company__name', 'contract__contractor__name', 'role__name']

class ChildCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'industry']
    search_fields = ['name', 'address', 'industry']

class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'service_domain', 'license_number']
    search_fields = ['name', 'address', 'service_domain', 'license_number']

admin.site.register(User, UserAdmin)
admin.site.register(ChildCompany, ChildCompanyAdmin)
admin.site.register(Contractor, ContractorAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractRole, ContractRoleAdmin)
admin.site.register(ContractAccess, ContractAccessAdmin)