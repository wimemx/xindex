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
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=15, null=False)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "User"


#class Manage(models.Model):


class Subsidiary_Type(models.Model):
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Types"
        verbose_name = "Type"


class Country(models.Model):
    AMERICA = 'AMERICA'
    CONTINENT = ((AMERICA, 'America'),
                 ('ASIA', 'Asia'),
                 ('EUROPA', 'Europa'),
                 ('OCEANIA', 'Oceania'),
                 ('AFRICA', 'Africa'))

    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
    code = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20, null=False)
    continent = models.CharField(choices=CONTINENT, default=AMERICA, max_length=7)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        verbose_name = "Country"


class State(models.Model):

    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
    country_id = models.ForeignKey(Country)
    name = models.CharField(max_length=20, null=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "States"
        verbose_name = "States"


class City(models.Model):
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
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
    states= models.ManyToManyField(State, blank=True, null=True)
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
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
    name = models.CharField(max_length=50, null=False) #------------------------------------max_length?
    types = models.ManyToManyField(Company_Type, blank=True, null=True) #---------------------------------------Type?
    parent_company = models.ForeignKey('Company', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=50, null=False)
    rfc = models.CharField(max_length=20, null=False)
    phone = models.CharField(max_length=50, null=False)
    zone = models.ManyToManyField(Zone, blank=True, null=True)
    staff = models.ManyToManyField(Xindex_User, blank=True, null=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def company_type(self):
        return ', '.join([a.name for a in self.types.all()])

    company_type.short_description = "Type"

    class Meta:
        verbose_name_plural = "Companies"
        verbose_name = "Company"


class Attribute(models.Model):
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Attributes"
        verbose_name = "Attribute"


class Question_Type(models.Model):
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
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
        verbose_name = "Question_Type"


class Question(models.Model):
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
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
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
    question = models.ForeignKey(Question)
    label = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    order = models.IntegerField()
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name_plural = "Options"
        verbose_name = "Option"


class Answer(models.Model):
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
    question = models.ForeignKey(Question)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    order = models.IntegerField()
    options = models.ManyToManyField(Option, null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.order

    class Meta:
        verbose_name_plural = "Answers"
        verbose_name = "Answer"


class Survey(models.Model):
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
    user = models.ForeignKey(Xindex_User)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    questions = models.ManyToManyField(Question, blank=True, null=True)
    active = models.BooleanField(default=True)
    date = models.DateField(default=datetime.now, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def survey_questions(self):
        return ', '.join([a.title for a in self.questions.all()])
    survey_questions.short_description = "Question"

    class Meta:
        verbose_name_plural = "Survey"
        verbose_name = "Survey"


class Indicator(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    type = models.CharField(max_length=20, null=False)
    min_value = models.DecimalField(max_digits=5, decimal_places=2)
    max_value = models.DecimalField(max_digits=5, decimal_places=2)
    threshold = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    attributes = models.ManyToManyField(Attribute, blank=True, null=True)
    questions = models.ManyToManyField(Question, blank=True, null=True)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Indicator"
        verbose_name = "Indicator"


class Service(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    picture = models.ImageField(upload_to="pictures/")
    moments = models.ManyToManyField('Moment', blank=True, null=True)
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
    service = models.ManyToManyField(Service, blank=True, null=True)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Business Unit"
        verbose_name = "Business Unit"


class Subsidiary(models.Model):
    #id = models.AutoField(primary_key=True, null=False, unique=True, \
    #                      blank=True)
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=50, null=False)
    #id_country = models.ForeignKey(Country)
    #id_state = models.ForeignKey(State)
    #id_city = models.ForeignKey(City)
    subsidiary_types = models.ManyToManyField(Subsidiary_Type, blank=True, null=True)
    business_unit = models.ManyToManyField(BusinessUnit, blank=True, null=True)
    #services = models.ManyToManyField(Service)
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
    attributes = models.ManyToManyField(Attribute, blank=True, null=True)
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