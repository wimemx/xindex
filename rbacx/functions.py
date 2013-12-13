# -*- coding: utf-8 -*-
import mandrill
import short_url
from xindex.models import Company
from rbacx.models import PermissionAssignment, UserRole, DataContextPermission,\
    Operation, Object

# my MANDRILL API KEY        hzuTlBSxNBabQDBkpTZveA


VIEW = "Ver"
CREATE = "Crear"
DELETE = "Eliminar"
UPDATE = "Editar"


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
    user_role = UserRole.objects.filter(
        user_id=user,
        role_id__status=True). \
        exclude(status=False)

    print user_role
    for eachUserRole in user_role:
        permission = PermissionAssignment.objects.filter(
            object_id__name=object_name,
            role_id=eachUserRole.role_id, operation_id=operation)
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


def mailing(new_user, content):
    try:
        mandrill_client = mandrill.Mandrill('hzuTlBSxNBabQDBkpTZveA')

        message = {
            'html': '<h2>Xindex Account</h2>'
                    + content,
            'subject': 'New member',
            'from_email': 'team@xindex.com.mx',
            'from_name': 'Xindex Account',
            'to': [
                {'email': new_user.email,
                 'name': new_user.first_name,
                 'type': 'to'}
            ],
            'important': True,
            'track_opens': True,
            'track_clicks': True,
            'auto_text': None,
            'auto_html': None,
            'tracking_domain': None,
            'signing_domain': None,
            'return_path_domain': None,
            'merge': True,
            'global_merge_vars': [
                {'content': 'merge1 content',
                 'name': 'GLOBAL MERGE'}],
            'merge_vars': [
                {'rcpt': 'martin_3-3@hotmail.com',
                 'vars': [
                     {'content': 'merge2 content',
                      'name': 'MARTIN ANDRADE'}
                 ]}
            ],
            'tags': ['prueba mailing'],
        }
        result = mandrill_client.messages.send(
            message=message,
            async=False)

        print result

    except mandrill.Error, e:

        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        raise
