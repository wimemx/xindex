import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Moment, Service, sbu_service, sbu_service_moment, \
    Zone, SubsidiaryBusinessUnit
from xindex.models import sbu_service_moment_attribute, Subsidiary, BusinessUnit
from xindex.forms import MomentForm


@login_required(login_url='/signin/')
def index(request):
    moments = Moment.objects.all().order_by('-date')
    template_vars = {"title": "Moments",
                     "moments": moments}
    request_context = RequestContext(request, template_vars)
    return render(request, 'moments/index.html', request_context)


@login_required(login_url='/signin/')
def detail(request, moment_id):
    try:
        moment = Moment.objects.get(pk=moment_id)
    except Moment.DoesNotExist:
        raise Http404
    return render(request, 'moments/detail.html', {'moment': moment})


@login_required(login_url='/signin/')
def add(request, service_id):
    print("Entrando al metodo")
    if request.method=='POST':
        form = MomentForm(request.POST)

        if form.is_valid():
            id_return = form.save()
            sbuService = sbu_service.objects.filter(id_service=service_id)

            for each_sbuService in sbuService:
                alias = id_return.name + ',' + each_sbuService.alias
                newSbuServiceMoment = sbu_service_moment.objects.create(
                    id_sbu_service=each_sbuService,
                    id_moment=id_return,
                    alias=alias
                )
                newSbuServiceMoment.save()

            return HttpResponseRedirect('/services/details/'+service_id)
        else:
            return HttpResponse("No")
    else:
        form = MomentForm()
        return render(request, "moments/add.html", {"formulario": form,
                                                    "service_id": service_id})


@login_required(login_url='/signin/')
def edit(request, moment_id):
    moment = Moment.objects.get(pk=moment_id)
    if request.POST:
        form = MomentForm(request.POST, instance=moment)
        if form.is_valid():
            form.save()
            return HttpResponse('Si')
    else:
        form = MomentForm(instance=moment)

    return render(request, "moments/edit.html", {"formulario": form,
                                                 "moment_id": moment_id})


@login_required(login_url='/signin/')
def remove(request, service_id, moment_id):

    try:
        moment = Moment.objects.get(pk=moment_id)
    except Moment.DoesNotExist:
        moment = False

    try:
        service = Service.objects.get(pk=service_id)
    except Service.DoesNotExist:
        service = False

    if moment and service:
        moment.active = False
        moment.save()

        mySbuServiceMoment = sbu_service_moment.objects.filter(
            id_moment_id=moment
        )

        for eachSBSM in mySbuServiceMoment:
            eachSBSM.delete()

        return HttpResponse('Si')
    else:
        return HttpResponse('No')


@login_required(login_url='/signin/')
def get_attributes(request):
    attributesList = []
    if request.POST:
        if 'zone' in request.POST and 'subsidiary' in request.POST \
                and 'business_unit' in request.POST and 'moment' in request.POST:
            if request.POST['zone'] == 'all' or request.POST['subsidiary'] == 'all' \
                    or request.POST['business_unit'] == 'all' or request.POST['moment'] == 'all':
                #get zone
                if request.POST['zone'] == 'all':
                    zone = Zone.objects.filter(active=True)
                else:
                    zone = Zone.objects.get(pk=int(request.POST['zone']))
                #get subsdiary
                if request.POST['subsidiary'] == 'all':
                    if isinstance(zone, Zone):
                        subsidiary = zone.subsidiary_set.filter(active=True)
                    else:
                        subsidiary = []
                        for z in zone:
                            for s in z.subsidiary_set.filter(active=True):
                                subsidiary.append(s)
                else:
                    subsidiary = Subsidiary.objects.get(active=True, pk=int(request.POST['subsidiary']))
                #get business unit
                if request.POST['business_unit'] == 'all':
                    business_unit = []
                    if isinstance(subsidiary, Subsidiary):
                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
                            business_unit.append(s_bu.id_business_unit)
                    else:
                        for s in subsidiary:
                            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=s):
                                coincidences = 0
                                for bu in business_unit:
                                    if bu == s_bu.id_business_unit:
                                        coincidences += 1
                                if coincidences == 0:
                                    business_unit.append(s_bu.id_business_unit)
                                else:
                                    pass
                else:
                    business_unit = BusinessUnit.objects.get(pk=int(request.POST['business_unit']))
                #get services
                if request.POST['service'] == 'all':
                    service = []
                    if isinstance(subsidiary, Subsidiary):
                        if isinstance(business_unit, BusinessUnit):
                            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                                    coincidences = 0
                                    for se in service:
                                        if se == s_bu_s.id_service:
                                            coincidences += 1
                                    if coincidences == 0:
                                        service.append(s_bu_s.id_service)
                        else:
                            for bu in business_unit:
                                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu):
                                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                                        coincidences = 0
                                        for se in service:
                                            if se == s_bu_s.id_service:
                                                coincidences += 1
                                        if coincidences == 0:
                                            service.append(s_bu_s.id_service)
                    else:
                        if isinstance(business_unit, BusinessUnit):
                            for sub in subsidiary:
                                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=business_unit):
                                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                                        coincidences = 0
                                        for se in service:
                                            if se == s_bu_s.id_service:
                                                coincidences += 1
                                        if coincidences == 0:
                                            service.append(s_bu_s.id_service)
                        else:
                            for sub in subsidiary:
                                for bu in business_unit:
                                    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=bu):
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                                            coincidences = 0
                                            for se in service:
                                                if se == s_bu_s.id_service:
                                                    coincidences += 1
                                            if coincidences == 0:
                                                service.append(s_bu_s.id_service)
                else:
                    service = Service.objects.get(pk=int(request.POST['service']))

                if request.POST['moment'] == 'all':
                    moment = []
                    if isinstance(subsidiary, Subsidiary):
                        if isinstance(business_unit, BusinessUnit):
                            if isinstance(service, Service):
                                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                            coincidences = 0
                                            for m in moment:
                                                if m == s_bu_s_m.id_moment:
                                                    coincidences += 1
                                            if coincidences == 0:
                                                moment.append(s_bu_s_m.id_moment)
                            else:
                                for serv in service:
                                    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=serv):
                                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                coincidences = 0
                                                for m in moment:
                                                    if m == s_bu_s_m.id_moment:
                                                        coincidences += 1
                                                if coincidences == 0:
                                                    moment.append(s_bu_s_m.id_moment)
                        else:
                            if isinstance(service, Service):
                                for bu in business_unit:
                                    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu):
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                coincidences = 0
                                                for m in moment:
                                                    if m == s_bu_s_m.id_moment:
                                                        coincidences += 1
                                                if coincidences == 0:
                                                    moment.append(s_bu_s_m.id_moment)
                            else:
                                for bu in business_unit:
                                    for ser in service:
                                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu):
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                    coincidences = 0
                                                    for m in moment:
                                                        if m == s_bu_s_m.id_moment:
                                                            coincidences += 1
                                                    if coincidences == 0:
                                                        moment.append(s_bu_s_m.id_moment)
                    else:
                        if isinstance(business_unit, BusinessUnit):
                            if isinstance(service, Service):
                                for sub in subsidiary:
                                    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                coincidences = 0
                                                for m in moment:
                                                    if m == s_bu_s_m.id_moment:
                                                        coincidences += 1
                                                if coincidences == 0:
                                                    moment.append(s_bu_s_m.id_moment)
                            else:
                                for sub in subsidiary:
                                    for serv in service:
                                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=business_unit):
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=serv):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                    coincidences = 0
                                                    for m in moment:
                                                        if m == s_bu_s_m.id_moment:
                                                            coincidences += 1
                                                    if coincidences == 0:
                                                        moment.append(s_bu_s_m.id_moment)
                        else:
                            if isinstance(service, Service):
                                for sub in subsidiary:
                                    for bu in business_unit:
                                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=bu):
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                    coincidences = 0
                                                    for m in moment:
                                                        if m == s_bu_s_m.id_moment:
                                                            coincidences += 1
                                                    if coincidences == 0:
                                                        moment.append(s_bu_s_m.id_moment)
                            else:
                                for sub in subsidiary:
                                    for bu in business_unit:
                                        for ser in service:
                                            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=bu):
                                                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                        coincidences = 0
                                                        for m in moment:
                                                            if m == s_bu_s_m.id_moment:
                                                                coincidences += 1
                                                        if coincidences == 0:
                                                            moment.append(s_bu_s_m.id_moment)
                else:
                    moment = Moment.objects.get(pk=int(request.POST['moment']))

                print 'kkkkkkkk'
                print moment
                print 'kkkkkkkk'

                #get attributes
                attributes = []
                if isinstance(subsidiary, Subsidiary):
                    if isinstance(business_unit, BusinessUnit):
                        if isinstance(service, Service):
                            if isinstance(moment, Moment):
                                #subsidiary IS an instance, business unit IS an instance, service IS an instance and moment IS an instance
                                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                                            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                coincidences = 0
                                                for attr in attributes:
                                                    if attr == s_bu_s_m_a.id_attribute:
                                                        coincidences += 1
                                                if coincidences == 0:
                                                    attributes.append(s_bu_s_m_a.id_attribute)
                                                    attributesList.append(
                                                        {
                                                            'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                            'attribute_name': s_bu_s_m_a.id_attribute.name
                                                        }
                                                    )
                            else:
                                #subsidiary IS an instance, business unit IS an instance, service IS an instance and moment IS NOT an instance
                                for m in moment:
                                    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=m):
                                                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                    coincidences = 0
                                                    for attr in attributes:
                                                        if attr == s_bu_s_m_a.id_attribute:
                                                            coincidences += 1
                                                    if coincidences == 0:
                                                        attributes.append(s_bu_s_m_a.id_attribute)
                                                        attributesList.append(
                                                            {
                                                                'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                'attribute_name': s_bu_s_m_a.id_attribute.name
                                                            }
                                                        )
                        else:
                            if isinstance(moment, Moment):
                                #subsidiary IS an instance, business unit IS an instance, service IS NOT an instance and moment IS an instance
                                for ser in service:
                                    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                                                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                    coincidences = 0
                                                    for attr in attributes:
                                                        if attr == s_bu_s_m_a.id_attribute:
                                                            coincidences += 1
                                                    if coincidences == 0:
                                                        attributes.append(s_bu_s_m_a.id_attribute)
                                                        attributesList.append(
                                                            {
                                                                'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                'attribute_name': s_bu_s_m_a.id_attribute.name
                                                            }
                                                        )
                            else:
                                #subsidiary IS an instance, business unit IS an instance, service IS NOT an instance and moment IS NOT an instance
                                for ser in service:
                                    for m in moment:
                                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=m):
                                                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                        coincidences = 0
                                                        for attr in attributes:
                                                            if attr == s_bu_s_m_a.id_attribute:
                                                                coincidences += 1
                                                        if coincidences == 0:
                                                            attributes.append(s_bu_s_m_a.id_attribute)
                                                            attributesList.append(
                                                                {
                                                                    'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                    'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                }
                                                            )
                    else:
                        if isinstance(service, Service):
                            if isinstance(moment, Moment):
                                #subsidiary IS an instance, business unit IS NOT an instance, service IS an instance and moment IS an instance
                                for bu in business_unit:
                                    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu):
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                                                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                    coincidences = 0
                                                    for attr in attributes:
                                                        if attr == s_bu_s_m_a.id_attribute:
                                                            coincidences += 1
                                                    if coincidences == 0:
                                                        attributes.append(s_bu_s_m_a.id_attribute)
                                                        attributesList.append(
                                                            {
                                                                'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                'attribute_name': s_bu_s_m_a.id_attribute.name
                                                            }
                                                        )
                            else:
                                #subsidiary IS an instance, business unit IS NOT an instance, service IS an instance and moment IS NOT an instance
                                for bu in business_unit:
                                    for m in moment:
                                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu):
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=m):
                                                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                        coincidences = 0
                                                        for attr in attributes:
                                                            if attr == s_bu_s_m_a.id_attribute:
                                                                coincidences += 1
                                                        if coincidences == 0:
                                                            attributes.append(s_bu_s_m_a.id_attribute)
                                                            attributesList.append(
                                                                {
                                                                    'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                    'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                }
                                                            )
                        else:
                            if isinstance(moment, Moment):
                                #subsidiary IS an instance, business unit IS NOT an instance, service IS NOT an instance and moment IS an instance
                                for bu in business_unit:
                                    for ser in service:
                                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu):
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                                                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                        coincidences = 0
                                                        for attr in attributes:
                                                            if attr == s_bu_s_m_a.id_attribute:
                                                                coincidences += 1
                                                        if coincidences == 0:
                                                            attributes.append(s_bu_s_m_a.id_attribute)
                                                            attributesList.append(
                                                                {
                                                                    'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                    'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                }
                                                            )
                            else:
                                #subsidiary IS an instance, business unit IS NOT an instance, service IS NOT an instance and moment IS NOT an instance
                                for bu in business_unit:
                                    for ser in service:
                                        for m in moment:
                                            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu):
                                                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=m):
                                                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                            coincidences = 0
                                                            for attr in attributes:
                                                                if attr == s_bu_s_m_a.id_attribute:
                                                                    coincidences += 1
                                                            if coincidences == 0:
                                                                attributes.append(s_bu_s_m_a.id_attribute)
                                                                attributesList.append(
                                                                    {
                                                                        'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                        'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                    }
                                                                )
                else:
                    if isinstance(business_unit, BusinessUnit):
                        if isinstance(service, Service):
                            if isinstance(moment, Moment):
                                #subsidiary IS NOT an instance, business unit IS an instance, service IS an instance and moment IS an instance
                                for sub in subsidiary:
                                    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=business_unit):
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                                                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                    coincidences = 0
                                                    for attr in attributes:
                                                        if attr == s_bu_s_m_a.id_attribute:
                                                            coincidences += 1
                                                    if coincidences == 0:
                                                        attributes.append(s_bu_s_m_a.id_attribute)
                                                        attributesList.append(
                                                            {
                                                                'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                'attribute_name': s_bu_s_m_a.id_attribute.name
                                                            }
                                                        )
                            else:
                                #subsidiary IS NOT an instance, business unit IS an instance, service IS an instance and moment IS NOT an instance
                                for sub in subsidiary:
                                    for m in moment:
                                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=business_unit):
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=m):
                                                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                        coincidences = 0
                                                        for attr in attributes:
                                                            if attr == s_bu_s_m_a.id_attribute:
                                                                coincidences += 1
                                                        if coincidences == 0:
                                                            attributes.append(s_bu_s_m_a.id_attribute)
                                                            attributesList.append(
                                                                {
                                                                    'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                    'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                }
                                                            )
                        else:
                            if isinstance(moment, Moment):
                                #subsidiary IS NOT an instance, business unit IS an instance, service IS NOT an instance and moment IS an instance
                                for sub in subsidiary:
                                    for ser in service:
                                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=business_unit):
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                                                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                        coincidences = 0
                                                        for attr in attributes:
                                                            if attr == s_bu_s_m_a.id_attribute:
                                                                coincidences += 1
                                                        if coincidences == 0:
                                                            attributes.append(s_bu_s_m_a.id_attribute)
                                                            attributesList.append(
                                                                {
                                                                    'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                    'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                }
                                                            )
                            else:
                                #subsidiary IS NOT an instance, business unit IS an instance, service IS NOT an instance and moment IS NOT an instance
                                for sub in subsidiary:
                                    for ser in service:
                                        for m in moment:
                                            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=business_unit):
                                                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=m):
                                                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                            coincidences = 0
                                                            for attr in attributes:
                                                                if attr == s_bu_s_m_a.id_attribute:
                                                                    coincidences += 1
                                                            if coincidences == 0:
                                                                attributes.append(s_bu_s_m_a.id_attribute)
                                                                attributesList.append(
                                                                    {
                                                                        'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                        'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                    }
                                                                )
                    else:
                        if isinstance(service, Service):
                            if isinstance(moment, Moment):
                                #subsidiary IS NOT an instance, business unit IS NOT an instance, service IS an instance and moment IS an instance
                                for sub in subsidiary:
                                    for bu in business_unit:
                                        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=bu):
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                                                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                        coincidences = 0
                                                        for attr in attributes:
                                                            if attr == s_bu_s_m_a.id_attribute:
                                                                coincidences += 1
                                                        if coincidences == 0:
                                                            attributes.append(s_bu_s_m_a.id_attribute)
                                                            attributesList.append(
                                                                {
                                                                    'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                    'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                }
                                                            )
                            else:
                                #subsidiary IS NOT an instance, business unit IS NOT an instance, service IS an instance and moment IS NOT an instance
                                for sub in subsidiary:
                                    for bu in business_unit:
                                        for m in moment:
                                            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=business_unit):
                                                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                                                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=m):
                                                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                            coincidences = 0
                                                            for attr in attributes:
                                                                if attr == s_bu_s_m_a.id_attribute:
                                                                    coincidences += 1
                                                            if coincidences == 0:
                                                                attributes.append(s_bu_s_m_a.id_attribute)
                                                                attributesList.append(
                                                                    {
                                                                        'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                        'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                    }
                                                                )
                        else:
                            if isinstance(moment, Moment):
                                #subsidiary IS NOT an instance, business unit IS NOT an instance, service IS NOT an instance and moment IS an instance
                                for sub in subsidiary:
                                    for bu in business_unit:
                                        for ser in service:
                                            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=bu):
                                                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                                                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                            coincidences = 0
                                                            for attr in attributes:
                                                                if attr == s_bu_s_m_a.id_attribute:
                                                                    coincidences += 1
                                                            if coincidences == 0:
                                                                attributes.append(s_bu_s_m_a.id_attribute)
                                                                attributesList.append(
                                                                    {
                                                                        'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                        'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                    }
                                                                )
                            else:
                                #subsidiary IS NOT an instance, business unit IS NOT an instance, service IS NOT an instance and moment IS NOT an instance
                                for sub in subsidiary:
                                    for bu in business_unit:
                                        for ser in service:
                                            for m in moment:
                                                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub, id_business_unit=bu):
                                                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=ser):
                                                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=m):
                                                            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                                                coincidences = 0
                                                                for attr in attributes:
                                                                    if attr == s_bu_s_m_a.id_attribute:
                                                                        coincidences += 1
                                                                if coincidences == 0:
                                                                    attributes.append(s_bu_s_m_a.id_attribute)
                                                                    attributesList.append(
                                                                        {
                                                                            'attribute_id': s_bu_s_m_a.id_attribute.id,
                                                                            'attribute_name': s_bu_s_m_a.id_attribute.name
                                                                        }
                                                                    )
                if len(attributesList) == 0:
                    json_response = {
                        'answer': False,
                        'attributes': attributesList
                    }
                else:
                    json_response = {
                        'answer': True,
                        'attributes': attributesList
                    }

                return HttpResponse(json.dumps(json_response))

            else:
                try:
                    zone = Zone.objects.get(pk=int(request.POST['zone']))
                    subsidiary = zone.subsidiary_set.get(
                        pk=int(request.POST['subsidiary'])
                    )
                    for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(
                            id_subsidiary=subsidiary,
                            id_business_unit=int(request.POST['business_unit'])
                    ):
                        for s_bu_s in sbu_service.objects.filter(
                                id_subsidiaryBU=subsidiary_business_unit):
                            for s_bu_s_m in sbu_service_moment.objects.filter(
                                    id_sbu_service=s_bu_s,
                                    id_moment=int(request.POST['moment'])):
                                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(
                                        id_sbu_service_moment=s_bu_s_m).order_by('id_attribute'):
                                    attributesList.append(
                                        {
                                            'attribute_id': s_bu_s_m_a.id_attribute.id,
                                            'attribute_name': s_bu_s_m_a.id_attribute.name
                                        }
                                    )
                    if len(attributesList) == 0:
                        pass
                    else:
                        json_response = {
                            'answer': True,
                            'attributes': attributesList
                        }
                        return HttpResponse(json.dumps(json_response))
                except Zone.DoesNotExist:
                    pass
        else:
            pass