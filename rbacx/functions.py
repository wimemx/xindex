# -*- coding: utf-8 -*-
import re
from datetime import date

from django.db.models.aggregates import Count
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson

from rbacx.models import PermissionAssignment, UserRole, DataContextPermission,\
    Operation, Object
from xindex.models import Company, Subsidiary, BusinessUnit, Service

"""
VIEW = Operation.objects.get(name="Ver")
CREATE = Operation.objects.get(name="Crear")
DELETE = Operation.objects.get(name="Eliminar")
UPDATE = Operation.objects.get(name="Modificar")
"""

def check_roles_permission(object_name):

    permissions = PermissionAssignment.objects.filter(
        object_id__name=object_name)
    role_operations = []
    for eachPermission in permissions:
        r_o = dict(role_id=eachPermission.role_id,
                   operation_id=eachPermission.operation_id)
        role_operations.append(r_o)
    return role_operations


def has_permission(user, operation, object_name):
    user_role = UserRole.objects.filter(user=user,
                                        role_id__status=True). \
        exclude(status=False)
    for eachUserRole in user_role:
        permission = PermissionAssignment.objects.filter(
            object_id__name=object_name,
            role=eachUserRole.role_id, operation_id=operation)
        if permission:
            return True
    return False


def get_all_companies_for_operation(operation, permission, user):
    if user.is_superuser:
        return Company.objects.filter(active=True)
    else:
        dataContext = DataContextPermission.objects.filter(
            user_role_id__user_id=user, subsidiary_id=None,
            business_unit_id=None, service_id=None)
        companies = []
        for eachDataContext in dataContext:
            permission_assignment = PermissionAssignment.objects.filter(
                role_id=eachDataContext.user_role_id.role_id,
                operation_id=operation,
                object_id__name=permission)
            if permission_assignment:
                companies.append(eachDataContext.company_id)
        return companies