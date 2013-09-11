import xindex.models
from django.contrib import admin


admin.site.register(xindex.models.Service)
admin.site.register(xindex.models.Answer)
admin.site.register(xindex.models.Attribute)
admin.site.register(xindex.models.City)
#admin.site.register(xindex.models.Companies)
admin.site.register(xindex.models.Company_Type)
admin.site.register(xindex.models.Country)
admin.site.register(xindex.models.Indicator)
#admin.site.register(xindex.models.Moment)
admin.site.register(xindex.models.Option)
admin.site.register(xindex.models.Question_Type)
admin.site.register(xindex.models.State)
#admin.site.register(xindex.models.Survey)
admin.site.register(xindex.models.Zone)
admin.site.register(xindex.models.Xindex_User)
admin.site.register(xindex.models.Question)
#admin.site.register(xindex.models.Subsidiary)
admin.site.register(xindex.models.Subsidiary_Type)
admin.site.register(xindex.models.BusinessUnit)
admin.site.register(xindex.models.Owner)


class SubsidiaryMe(admin.ModelAdmin):
    list_display = ['company', 'name', 'subsidiary_zone','active']
    list_filter = ['company']


class MomentMe(admin.ModelAdmin):
    list_display = ['name', 'previous_moment']
    list_filter = ['name']


class SurveyMe(admin.ModelAdmin):
    list_display = ['user', 'name', 'survey_questions']
    list_filter = ['user']


class CompanyMe(admin.ModelAdmin):
    list_display = ['name', 'company_type', 'active']
    list_filter = ['types']


admin.site.register(xindex.models.Company, CompanyMe)
admin.site.register(xindex.models.Moment, MomentMe)
admin.site.register(xindex.models.Subsidiary, SubsidiaryMe)
admin.site.register(xindex.models.Survey, SurveyMe)