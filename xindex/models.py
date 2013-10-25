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
    email = models.CharField(max_length=50, null=True, blank=True)
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
    name = models.CharField(max_length=50, null=False)
    types = models.ManyToManyField(Company_Type, blank=True, null=True)
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
        return ', '.join([a.name for a in self.types.all()])

    company_type.short_description = "Type"

    class Meta:
        verbose_name_plural = "Companies"
        verbose_name = "Company"


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

    def get_value(self):
        if self.value == int(self.value):
            self.value = int(self.value)
        return self.value

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
    description = models.TextField(null=True, blank=True)
    questions = models.ManyToManyField(Question, blank=True, null=True)
    step = models.IntegerField(max_length=2, null=True, blank=True)
    picture = models.CharField(max_length=50, null=True, blank=True,
                               default="No image")
    available = models.BooleanField(default=True)
    configuration = models.TextField()
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


class Question_Attributes(models.Model):
    question_id = models.ForeignKey(Question)
    attribute_id = models.ForeignKey(Attributes, null=True)
    moment_id = models.ForeignKey('Moment', null=True)
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
    subsidiary = models.ForeignKey('Subsidiary', null=False)
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
    address = models.CharField(max_length=50, null=False)
    rfc = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=50, null=False)
    country_id = models.ForeignKey(Country)
    state_id = models.ForeignKey(State)
    city_id = models.ForeignKey(City, null=True, blank=True)
    subsidiary_types = models.ManyToManyField(Subsidiary_Type, blank=True, null=True)
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
    user = models.ForeignKey(Xindex_User);
    question = models.ForeignKey(Question);
