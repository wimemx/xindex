from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Company_Type(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Company_Types"
        verbose_name = "Company_Type"


class Xindex_User(models.Model):
    """
    (User or Xindex User)
    Informacion de perfil

    """
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    #Status         |
    #Username       |-->
    #Password       |

    def __unicode__(self):
        return self.user.username + "-" + self.user.first_name + " " + self \
            .user.last_name

    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "User"


class Subsidiary_Type(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subsidiary_Types"
        verbose_name = "Subsidiary_Type"


class Country(models.Model):
    AMERICA = 'AMERICA'
    CONTINENT = ((AMERICA, 'America'),
                 ('ASIA', 'Asia'),
                 ('EUROPA', 'Europa'),
                 ('OCEANIA', 'Oceania'),
                 ('AFRICA', 'Africa'))

    code = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20, null=False)
    continent = models.CharField(choices=CONTINENT, default=AMERICA,
                                 max_length=7)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        verbose_name = "Country"


class State(models.Model):

    country_id = models.ForeignKey(Country)
    name = models.CharField(max_length=20, null=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "States"
        verbose_name = "States"


class City(models.Model):

    state = models.ForeignKey(State)
    name = models.CharField(max_length=20, null=False)
    lat = models.DecimalField(max_digits=20, decimal_places=10)
    long = models.DecimalField(max_digits=20, decimal_places=10)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"
        verbose_name = "Cities"


class Zone(models.Model):
    countries = models.ManyToManyField(Country, blank=True, null=True)
    states = models.ManyToManyField(State, blank=True, null=True)
    cities = models.ManyToManyField(City, blank=True, null=True)
    name = models.CharField(max_length=20, null=False)
    description = models.TextField()
    parent_zone = models.ForeignKey('Zone', null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Zones"
        verbose_name = "Zone"


class Company(models.Model):

    name = models.CharField(max_length=50, null=False)
    types = models.ForeignKey(Company_Type, blank=True, null=True)
    parent_company = models.ForeignKey('Company', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=50, null=False)
    rfc = models.CharField(max_length=20, null=False)
    phone = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=True, blank=True)
    zone = models.ManyToManyField(Zone, blank=True, null=True)
    staff = models.ManyToManyField(Xindex_User, blank=True, null=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def company_type(self):
        return ', '.join([a.name for a in self.types.name])

    company_type.short_description = "Type"

    class Meta:
        verbose_name_plural = "Companies"
        verbose_name = "Company"


class Question_Type(models.Model):

    name = models.CharField(max_length=20, null=False)
    help_text = models.TextField()
    description = models.TextField()
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Question_Types"
        verbose_name = "Question Type"


class Question(models.Model):

    user = models.ForeignKey(Xindex_User)
    title = models.CharField(max_length=150)
    description = models.TextField()
    type = models.ForeignKey(Question_Type)
    parent_question = models.ForeignKey('Question', blank=True, null=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Questions"
        verbose_name = "Question"


class Option(models.Model):

    question = models.ForeignKey(Question)
    label = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    order = models.IntegerField()
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.label

    def get_value(self):
        if self.value == int(self.value):
            self.value = int(self.value)
        return self.value

    class Meta:
        verbose_name_plural = "Options"
        verbose_name = "Option"


class Answer(models.Model):
    question = models.ForeignKey(Question)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    order = models.IntegerField()
    options = models.ManyToManyField(Option, null=True, blank=True)
    client = models.ForeignKey('Client', null=True, blank=True)
    client_activity = models.ForeignKey('ClientActivity', null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.order)

    class Meta:
        verbose_name_plural = "Answers"
        verbose_name = "Answer"


class Survey(models.Model):

    user = models.ForeignKey(Xindex_User)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)
    questions = models.ManyToManyField(Question, blank=True, null=True)
    step = models.IntegerField(max_length=2, null=True, blank=True)
    picture = models.CharField(max_length=50, null=True, blank=True,
                               default="No image")
    available = models.BooleanField(default=True)
    configuration = models.TextField()
    business_unit_id = models.ForeignKey('BusinessUnit', blank=True, null=False)
    service_id = models.ForeignKey('Service', blank=True, null=False)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def survey_questions(self):
        return ', '.join([a.title for a in self.questions.all()])
    survey_questions.short_description = "Question"

    class Meta:
        verbose_name_plural = "Surveys"
        verbose_name = "Survey"


class Attributes(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    threshold = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Attributes"
        verbose_name = "Attribute"


class Question_sbu_s_m_a(models.Model):
    question_id = models.ForeignKey(Question)
    #sbu_s_m_a_id = models.ForeignKey('sbu_service_moment_attribute', null=True)
    sbu_s_m_a_id = models.ManyToManyField('sbu_service_moment_attribute', null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.weight)

    class Meta:
        verbose_name_plural = "Preguntas-Atributos"
        verbose_name = "Pregunta-Atributo"


class Service(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    #picture = models.ImageField(upload_to="pictures/")
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Services"
        verbose_name = "Service"


class BusinessUnit(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    active = models.BooleanField(default=True)
    date = models.DateTimeField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Business Unit"
        verbose_name = "Business Unit"


class Subsidiary(models.Model):

    company = models.ForeignKey(Company)
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    rfc = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=50, null=False)
    country_id = models.ForeignKey(Country)
    state_id = models.ForeignKey(State)
    city_id = models.ForeignKey(City, null=True, blank=True)
    subsidiary_types = models.ForeignKey(Subsidiary_Type, blank=True, null=True)
    zone = models.ForeignKey(Zone, blank=True, null=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def subsidiary_zone(self):
        return ', '.join([a.name for a in self.zone.all()])
    subsidiary_zone.short_description = "Zone"

    class Meta:
        verbose_name_plural = "Subsidiaries"
        verbose_name = "Subsidiary"


class Owner(models.Model):
    name = models.CharField(max_length=50, null=False)
    type = models.CharField(max_length=50, null=False)
    subsidiary = models.ForeignKey(Subsidiary)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Owners"
        verbose_name = "Owner"


class Moment(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    previous_moment = models.ForeignKey('Moment', blank=True, null=True)
    attributes = models.ManyToManyField(Attributes, blank=True, null=True)
    owners = models.ManyToManyField(Owner, blank=True, null=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        #order_with_respect_to = "previous_moment"
        verbose_name_plural = "Moments"
        verbose_name = "Moment"


class Catalog(models.Model):
    user = models.ForeignKey('Xindex_User')
    question = models.ForeignKey(Question)


class Client(models.Model):
    SEX = (('M', 'Masculino'), ('F', 'Femenino'))

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(choices=SEX, default='M', max_length=1,
                           blank=True, null=True)
    email = models.EmailField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    company = models.ForeignKey('Company', blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2,
                                 blank=True, null=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.first_name)


class ClientActivity(models.Model):
    STATUS = (('A', 'Answered'), ('NA', 'Not Answered'))

    date = models.DateField(default=datetime.now, blank=True, null=True)
    client = models.ForeignKey('Client', null=True, blank=True)
    subsidiary = models.ForeignKey('Subsidiary', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True)
    service = models.ForeignKey('Service', null=True, blank=True)
    survey = models.ForeignKey('Survey', null=True, blank=True)
    status = models.CharField(choices=STATUS, default='NA', max_length=2,
                              blank=True, null=True)
    code = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.client.first_name
    

class Cumulative_Report(models.Model):
    #id_company = models.ForeignKey(Company, blank=True, null=True)
    #id_zone = models.ForeignKey(Zone, blank=True, null=True)
    id_subsidiary = models.ForeignKey(Subsidiary, blank=True, null=True)
    id_business_unit = models.ForeignKey(BusinessUnit, blank=True, null=True)
    id_service = models.ForeignKey(Service, blank=True, null=True)
    id_moment = models.ForeignKey(Moment, blank=True, null=True)
    id_attribute = models.ForeignKey(Attributes, blank=True, null=True)
    grade = models.DecimalField(max_digits=8, decimal_places=5)
    date = models.DateField(default=datetime.now, blank=True, null=True)

    def __unicode__(self):
        return str(self.grade)

    class Meta:
        verbose_name_plural = "Reportes Historicos"
        verbose_name = "Reporte Historico"


class SubsidiaryBusinessUnit(models.Model):
    id_subsidiary = models.ForeignKey(Subsidiary, blank=True, null=True)
    id_business_unit = models.ForeignKey(BusinessUnit, blank=True, null=True)
    alias = models.CharField(max_length=260, blank=True, null=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.alias

    class Meta:
        verbose_name_plural = "Subsidiarias-UnidadesServicio"
        verbose_name = "Subsidiaria-UnidadServicio"


class sbu_service(models.Model):
    id_subsidiaryBU = models.ForeignKey(SubsidiaryBusinessUnit, blank=True, null=True)
    id_service = models.ForeignKey(Service, blank=True, null=True)
    alias = models.CharField(max_length=260, blank=True, null=True)

    def __unicode__(self):
        return self.alias

    class Meta:
        verbose_name_plural = "SBU-Services"
        verbose_name = "SBU-Service"


class sbu_service_moment(models.Model):
    id_sbu_service = models.ForeignKey(sbu_service, blank=True, null=True)
    id_moment = models.ForeignKey(Moment, blank=True, null=True)
    alias = models.CharField(max_length=260, blank=True, null=True)

    def __unicode__(self):
        return self.id_sbu_service.__unicode__()+'-'+self.id_moment.name

    class Meta:
        verbose_name_plural = "SBU-Services-Moments"
        verbose_name = "SBU-Service-Moment"


class sbu_service_moment_attribute(models.Model):
    id_sbu_service_moment = models.ForeignKey(sbu_service_moment, blank=True, null=True)
    id_attribute = models.ForeignKey(Attributes, blank=True, null=True)
    alias = models.CharField(max_length=260, blank=True, null=True)

    def __unicode__(self):
        return self.id_sbu_service_moment.__unicode__()+'-'+str(self.id_attribute)

    class Meta:
        verbose_name_plural = "SBU-Services-Moments-Attributes"
        verbose_name = "SBU-Service-Moment-Attribute"
