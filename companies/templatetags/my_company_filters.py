from django import template
from xindex.models import Xindex_User

register = template.Library()


@register.filter(name='get_logo_name')
def get_logo_name(user):
    xindex_user = Xindex_User.objects.get(user=user)
    logo_name = 'xindex-logo.png'
    for company in xindex_user.company_set.filter(active=True):
        if company.logo != 'No image':
            logo_name = company.logo

    return logo_name