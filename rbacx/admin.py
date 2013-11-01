import rbacx.models
from django.contrib import admin

admin.site.register(rbacx.models.ExtendedUser)
#admin.site.register(rbacx.models.UserProfile)
admin.site.register(rbacx.models.Operation)
admin.site.register(rbacx.models.Object)
admin.site.register(rbacx.models.Role)
admin.site.register(rbacx.models.PermissionAssignment)
admin.site.register(rbacx.models.UserRole)


class DataContextPermissionAdmin(admin.ModelAdmin):
    list_display = ['user_role_id', 'company_id', 'subsidiary_id',
                    'service_id']
    list_filter = ['user_role_id']

admin.site.register(rbacx.models.DataContextPermission,
                    DataContextPermissionAdmin)