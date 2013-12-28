from tenantCustomer.models import Customer_info
from django.contrib import admin

class CostumerAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain_url',   \
                    'schema_name', 'mail', 'status',\
                    'paid_until', 'registered_on')

    list_filter = ['status']
    search_fields = ['name']
    date_hierarchy = 'paid_until'

admin.site.register(Customer_info, CostumerAdmin)
