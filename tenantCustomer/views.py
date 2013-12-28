#-*- coding: utf-8 -*-


import re
import datetime
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from tenantCustomer.models import Customer_info
from django.template import RequestContext, loader
from django.core.validators import email_re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from xindex.models import Xindex_User

BASE_DOMAIN = 'xindex.192.168.1.108.xip.io'

"""
    AUXILIAR FUNCTIONS
"""

def is_valid_email(email):
    """ check if a string is a valid email address
    django dependant
    :param email: - the string to evaluate
    :return: boolean, True if valid, False if not
    """

    return True if email_re.match(email) else False

def validate_string(strng):
    """Checks for non word chars in a unicode string
    :param strng: string object, the string to validate
    :return: boolean, True if valid, False if not
    """
    if not isinstance(strng, str) and not isinstance(strng, unicode):
        return False
    pattern = re.compile(r'[^\w\s\-\'\."]', re.UNICODE)
    string_arr = strng.split(" ")
    for i in string_arr:
        if i == "" or pattern.search(i):
            return False
    return True

def mail_to(email, content):
    subject = "Tu nueva cuenta en xindex"
    return True

"""
    VIEWS
"""

def tenant_index(request):
    template = loader.get_template('tenantCustomer/index.html')
    context = RequestContext(request, {
        'app_name': 'Xindex',
        })
    return HttpResponse(template.render(context))


def register(request):
    template_variables = {}
    if request.method == 'POST':
        name = request.POST['name']
        mail = request.POST['mail']
        passw = request.POST['pass']
        passb = request.POST['passb']
        accept = request.POST.get('accept', False)

        if accept == False:
            template_variables['creation_status'] = 'Failure'
            template_variables['error_message'] = 'Debes de aceptar los terminos y condiciones'
        if passw != passb or passw == "":
            template_variables['creation_status'] = 'Failure'
            template_variables['error_message'] = 'Las contraseñas no coinciden'
        if is_valid_email(mail) == False:
            template_variables['creation_status'] = 'Failure'
            template_variables['error_message'] = 'El mail es inválido'
        if name == "" or validate_string(name) == False:
            template_variables['creation_status'] = 'Failure'
            template_variables['error_message'] = 'Nombre de usuario invalido'
        aux = template_variables.get('creation_status', '')
        if aux != 'Failure':
            try:
                pay_day = datetime.datetime.today() + datetime.timedelta(days=15)
                domain = name.lower() + "." + BASE_DOMAIN
                s_name = name.lower()
                new_tenant, created = \
                    Customer_info.objects.get_or_create(domain_url=domain,              \
                        schema_name=s_name, defaults={'name': name, 'role': 'owner',    \
                        'paid_until': pay_day, 'status': False, 'mail': mail}
                    )
            except DatabaseError:
                   connection._rollback()
                   template_variables['creation_status'] = 'Failure'
                   template_variables['error_message'] = 'El nombre de usuario solicitado ' \
                                                         'no esta disponible, intente de nuevo'
            else:
                connection.set_tenant(new_tenant)
                user = User(username=name, is_superuser=True)
                user.save()
                user.set_password(passw)
                user.save()
                #saving xindex user
                x_user = Xindex_User()
                x_user.user = user
                x_user.first_name = name
                x_user.save()

                template_variables['creation_status'] = 'Success'
                template_variables['name'] = name
                template_variables['mail'] = mail
                template_variables['domain'] = domain
                content = "Bienvenido a xindex! sus datos son: \n"
                content += "Nombre de usuario: " + name + "\n"
                content += "Dominio: " + domain + "\n"
                mail_to(mail, content)
    template = loader.get_template('tenantCustomer/register.html')
    context = RequestContext(request, template_variables)
    return HttpResponse(template.render(context))

def manager(request):
    template_variables = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
           login(request, user)
           template_variables['status'] = 'Success'
           context = RequestContext(request, template_variables)
           return HttpResponseRedirect('/manager_list/')
        else:
            template_variables['status'] = 'Failure'
            template_variables['error'] = ' datos de usuario no validos'
    template = loader.get_template('tenantCustomer/manager_login.html')
    context = RequestContext(request, template_variables)
    return HttpResponse(template.render(context))

@login_required
def manager_list(request):
    template_variables = {}
    template_variables['status'] = 'OK'
    transaction = request.POST.get('bulk')
    context = RequestContext(request, template_variables)
    if transaction == "Aplicar":
        ids = request.POST.getlist('client_ids')
        action = request.POST.get('action_id')
        for id in ids:
            tmp_obj = Customer_info.objects.get(pk=id)
            if action == 1:
                tmp_obj.status = True
                tmp_obj.save()
            if action == 2:
                tmp_obj.status = False
                tmp_obj.save()
            if action == 3:
                tmp_obj.delete()
    else:
        client_list = Customer_info.objects.all()
        p = Paginator(client_list, 5)
        page_number = request.GET.get('page')
        try:
            clients = p.page(page_number)
        except PageNotAnInteger:
            clients = p.page(1)
        except EmptyPage:
            clients = p.page(p.num_pages)
        template_variables['clients'] = clients
        context = RequestContext(request, template_variables)
    template = loader.get_template('tenantCustomer/manager_list.html')
    return HttpResponse(template.render(context))
