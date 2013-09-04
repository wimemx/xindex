# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext

def index(request):
    template_vars = {
        #vars
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("xindex/index.html", request_context)