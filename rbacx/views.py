import random
from django.shortcuts import render_to_response, HttpResponse, \
    HttpResponseRedirect, get_object_or_404
from django.template.context import RequestContext
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.utils import simplejson
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from rbacx.functions import mailing
from xindex.models import Company, Subsidiary, BusinessUnit, Service, \
    Xindex_User
from rbacx.models import Operation, Role


VIEW = "Ver"
CREATE = "Crear"
DELETE = "Eliminar"
UPDATE = "Editar"


@login_required(login_url='/signin/')
def profile(request):
    user = request.user
    extendedInfo = Xindex_User.objects.get(user=user)

    template_vars = {"user": user,
                     "extendedInfo": extendedInfo}
    request_context = RequestContext(request, template_vars)
    return render_to_response("rbac/profile.html", request_context)


@login_required(login_url='/signin/')
def control_panel(request):
    user = request.user
    extendedInfo = Xindex_User.objects.get(user=user)

    template_vars = {"user": user,
                     "extendedInfo": extendedInfo}
    request_context = RequestContext(request, template_vars)
    return render_to_response("rbac/control_panel.html", request_context)


@login_required(login_url='/signin/')
def user_list(request):
    user = request.user
    extendedInfo = Xindex_User.objects.get(user=user)

    template_vars = {}
    request_context = RequestContext(request, template_vars)
    return render_to_response("rbac/user_list.html", request_context)


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def getUsersInJson(request):
    users = {'users': []}

    userQuery = User.objects.filter(is_active=True)
    for eachUser in userQuery:
        users['users'].append(
            {
                "name": eachUser.first_name,
                "surname": eachUser.last_name,
                "email": eachUser.email,
                "role": "Rol",
                "actions": eachUser.id
            }
        )

    return HttpResponse(simplejson.dumps(users))


@login_required(login_url='/signin/')
def edit_profile(request, action):
    todo = ''
    content = ''
    exclusive_content = ''
    action_exclusive_content = ''

    user = request.user
    basicInfo = User.objects.get(pk=user.id)
    extendedInfo = Xindex_User.objects.get(user=user)

    if action == "1":
        todo = 'Nombre'
        action_exclusive_content = 'Apellido'

        content = basicInfo.first_name
        exclusive_content = basicInfo.last_name

    elif action == "2":
        todo = 'Email'

        content = basicInfo.email

    elif action == "3":
        todo = 'Password'

    elif action == "4":
        todo = 'Telefono'

        content = extendedInfo.phone

    if request.POST:
        content = request.POST.getlist('content-to-change')
        content2 = request.POST.getlist('content-to-change-2')
        content_id = request.POST.getlist('content-id')

        idContent = ''
        contentOne = ''
        contentTwo = ''

        for eachIdContent in content_id:
            idContent = eachIdContent

        for eachContent in content:
            contentOne = eachContent

        for eachContent2 in content2:
            contentTwo = eachContent2

        if idContent == "1":
            request.user.first_name = contentOne
            request.user.last_name = contentTwo
            request.user.save()

        if idContent == "2":
            request.user.email = contentOne
            request.user.save()

        if idContent == "3":
            if contentOne == contentTwo:
                request.user.set_password(contentTwo)
                request.user.save()

        if idContent == "4":
            extendedInfo.phone = contentOne
            extendedInfo.save()

        return HttpResponseRedirect('/profile/')

    else:
        template_vars = {"action_content": todo,
                         "action_id": action,
                         "content": content,
                         "exclusive_content": exclusive_content,
                         "action_exclusive_content": action_exclusive_content}

        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/edit_profile.html", request_context)


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def create_user(request):

    if request.POST:
        name = request.POST['user_name']
        surname = request.POST['user_surname']
        username = name[:1]

        if len(surname) > 10:
            username += surname[:10]
        else:
            username += surname

        username = str(username)
        username = str.lower(username)
        username += str(random.randint(1, 9) + random.randrange(100, 10000, 3))
        email = request.POST['user_email']

        password = username[:2]
        password += str(random.randint(1, 9) + random.randrange(100, 10000, 3))

        phone = request.POST['user_phone']

        new_user = User.objects.create_user(username,
                                            email, password)

        new_user.first_name = name
        new_user.last_name = surname
        new_user.is_active = True

        new_user.save()

        content = 'Username:' + username + ' - Password:' + password

        mailing(new_user, content)
        #email = EmailMessage('Xindex Account', content, to=[new_user.email])
        #email.send()

        new_xindexUser = Xindex_User.objects.create(user=new_user,
                                                    first_name=name,
                                                    last_name=surname,
                                                    email=new_user.email,
                                                    phone=phone)

        new_xindexUser.save()

        return HttpResponseRedirect('/user_list/')

    else:
        roles = Role.objects.filter(status=True)
        template_vars = {"roles": roles}

        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/add_user.html", request_context)


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):

    if request.user.id != user_id:
        user = User.objects.get(pk=user_id)
        user.is_active = False
        user.save()

        #xindexUser = Xindex_User.objects.get(user=user)
        return HttpResponse('Si')
    else:
        return HttpResponse('No puedes eliminar tu propia cuenta')


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    userDjango = User.objects.get(pk=user_id)
    userXindex = Xindex_User.objects.get(user=userDjango)

    if request.POST:
        userDjango.first_name = request.POST['user_name']
        userDjango.last_name = request.POST['user_surname']
        userDjango.email = request.POST['user_email']
        userDjango.save()

        userXindex.phone = request.POST['user_phone']
        userXindex.save()

        return HttpResponseRedirect('/user_list/')
    else:
        template_vars = {'id': userDjango.id,
                         'name': userDjango.first_name,
                         'surname': userDjango.last_name,
                         'email': userDjango.email,
                         'phone': userXindex.phone}

        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/edit_user.html", request_context)


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def user_profile(request, user_id):
    userDjango = User.objects.get(pk=user_id)
    userXindex = Xindex_User.objects.get(user=userDjango)

    template_vars = {'id': userDjango.id,
                     'name': userDjango.first_name,
                     'surname': userDjango.last_name,
                     'email': userDjango.email,
                     'phone': userXindex.phone}

    request_context = RequestContext(request, template_vars)
    return render_to_response("rbac/user_profile.html", request_context)


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def my_account(request):

    user = request.user
    xindexUser = Xindex_User.objects.get(user=user)

    try:
        company = Company.objects.get(staff=xindexUser)
    except Company.MultipleObjectsReturned:
        company = Company.objects.filter(staff=xindexUser)[:1]

    template_vars = {
        'company': company
    }

    request_context = RequestContext(request, template_vars)
    return render_to_response("rbac/my_account.html", request_context)


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def edit_account(request, data):

    user = request.user
    xindexUser = Xindex_User.objects.get(user=user)
    data_to_change = False
    data_label = ''

    try:
        company = Company.objects.get(staff=xindexUser)
    except Company.MultipleObjectsReturned:
        company = Company.objects.filter(staff=xindexUser)[:1]

    if request.POST:
        if data == 'company_name':
            if 'company_name' in request.POST:
                company.name = request.POST['company_name']
        elif data == 'company_address':
            if 'company_address' in request.POST:
                company.address = request.POST['company_address']
        elif data == 'company_phone':
            if 'company_phone' in request.POST:
                company.phone = request.POST['company_phone']
        elif data == 'company_rfc':
            if 'company_rfc' in request.POST:
                company.rfc = request.POST['company_rfc']
        company.save()
        return HttpResponseRedirect('/my_account/')
    else:
        #check data to change
        if data == 'company_name':
            data_label = 'Nombre de la compa&ntilde;ia'
            data_to_change = company.name
        elif data == 'company_address':
            data_label = 'Direcci&oacute;n de la compa&ntilde;ia'
            data_to_change = company.address
        elif data == 'company_phone':
            data_label = 'Telefono de la compa&ntilde;ia'
            data_to_change = company.phone
        elif data == 'company_rfc':
            data_label = 'RFC de la compa&ntilde;ia'
            data_to_change = company.rfc

        template_vars = {
            'data_label': data_label,
            'data_to_change': data_to_change,
            'data': data
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/edit_account.html", request_context)

