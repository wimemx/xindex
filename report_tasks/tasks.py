from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from decimal import *
from xindex.models import Question_Attributes
from xindex.models import Moment


#Report for Jan, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov and Dec
@periodic_task(run_every=crontab(minute="01",
                                 hour="08", day_of_month="30",
                                 month_of_year="1, 3-12"))
def save_report_by_month():
    xindex_attribute = Decimal(0)
    xindex_moment = Decimal(0)
    xindex_service = Decimal(0)
    xindex_business_unit = Decimal(0)
    xindex_subsidiary = Decimal(0)

    #Save xindex for every moment by month
    for moment in Moment.objects.all():
        #Get the relations of the moment
        relations_maq = Question_Attributes.objects.filter(moment_id=moment.id)

        #Get promoters, passives and detractors by attribute
        total_promoters = 0
        total_passives = 0
        total_detractors = 0
        total_answers = 0
        for relation in relations_maq.all():
            for answer in relation.question_id.answer_set.all():
                total_answers += 1
                if answer.value == 10 or answer.value == 9:
                    total_promoters += 1
                elif answer.value == 8 or answer.value == 7:
                    total_passives += 1
                elif 1 <= answer.value <= 6:
                    total_detractors += 1
        #Set the precision for decimal numbers
        getcontext().prec = 5
        xindex_moment = ((Decimal(total_promoters - total_detractors)) /
                         (Decimal(total_promoters +
                                  total_passives + total_detractors)
                         )
                        )*Decimal(100)

        #Get date



#Report for Feb
@periodic_task(run_every=crontab(minute="01",
                                 hour="08",
                                 day_of_month="28",
                                 month_of_year="2"))
def save_report_by_month():
    print 'Saving report by month feb'
