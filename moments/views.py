import json
from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Moment, Service, sbu_service, sbu_service_moment, \
    Zone, SubsidiaryBusinessUnit
from xindex.models import sbu_service_moment_attribute
from xindex.forms import MomentForm


def index(request):
    moments = Moment.objects.all().order_by('-date')
    template_vars = {"title": "Moments",
                     "moments": moments}
    request_context = RequestContext(request, template_vars)
    return render(request, 'moments/index.html', request_context)


def detail(request, moment_id):
    try:
        moment = Moment.objects.get(pk=moment_id)
    except Moment.DoesNotExist:
        raise Http404
    return render(request, 'moments/detail.html', {'moment': moment})


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


def get_attributes(request):
    attributesList = []
    if request.POST:
        if 'zone' in request.POST and 'subsidiary' in request.POST \
            and 'business_unit' in request.POST and 'moment' in request.POST:

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