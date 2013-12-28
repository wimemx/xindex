from django.db import models
from tenant_schemas.models import TenantMixin

class Customer_info(TenantMixin):

    name            = models.CharField(max_length=128)
    role            = models.CharField(max_length=10, default="Owner")
    package         = models.CharField(max_length=128, default="Prueba")
    mail            = models.EmailField()

    paid_until      = models.DateField()
    registered_on   = models.DateField(auto_now_add=True)
    status        = models.BooleanField()

    auto_create_schema = True

    def save(self, *args, **kargs):
        super(Customer_info, self).save(*args, **kargs)
