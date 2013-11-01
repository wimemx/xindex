import django.contrib.auth.models
from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime

from xindex.models import Company, Subsidiary, BusinessUnit, Service


class ExtendedUser(models.Model):
    """
    Informacion adicional del usuario

    """
    user_id = models.OneToOneField(User, on_delete=models.PROTECT)
    activation_key = models.CharField(max_length=128)
    first_visit = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.user_id.username + "-" + str(self.first_visit)


class Operation(models.Model):
    """
    Acciones que se pueden realizar sobre un objeto
    (crear, modificar, eliminar, ver, etc.)

    """
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Role(models.Model):
    """
    Roles que seran asignados en el sistema

    """
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=256, null=True, blank=True)
    importance = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Object(models.Model):
    """
    Objetos del sistema

    """
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=256, null=True, blank=True)
    access_point = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class PermissionAssignment(models.Model):
    """
    Asignacion de permisos a roles

    """
    role_id = models.ForeignKey(Role, on_delete=models.PROTECT)
    operation_id = models.ForeignKey(Operation, on_delete=models.PROTECT)
    object_id = models.ForeignKey(Object, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.role_id.name + "-" + self.operation_id.name \
            + "-" + self.object_id.name


class UserRole(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    role_id = models.ForeignKey(Role, on_delete=models.PROTECT)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user_id.username + "-" + self.role_id.name

    class Meta:
        unique_together = ('user_id', 'role_id')


class DataContextPermission(models.Model):
    """
    Contexto de asignacion de permisos
    (Un rol asignado a un usuario puede tener privilegios en distintos niveles
    dentro de la jerarquia de administracion)

    """
    user_role_id = models.ForeignKey(UserRole, on_delete=models.PROTECT)
    company_id = models.ForeignKey(Company, on_delete=models.PROTECT,
                                   blank=True, null=True, default=None)
    subsidiary_id = models.ForeignKey(Subsidiary, on_delete=models.PROTECT,
                                      blank=True, null=True, default=None)
    business_unit_id = models.ForeignKey(BusinessUnit, on_delete=models.PROTECT,
                                         blank=True, null=True, default=None)
    service_id = models.ForeignKey(Service, on_delete=models.PROTECT,
                                   blank=True, null=True)

    def __unicode__(self):
        """
        S = Subject = Persona (Usuario)

        """
        s = self.user_role_id.user_id.username

        if self.company_id:
            s += "-" + self.company_id.name
        if self.subsidiary_id:
            s += "-" + self.subsidiary_id.name
        if self.business_unit_id:
            s += "-" + self.business_unit_id.name
        if self.service_id:
            s += "-" + self.service_id.name