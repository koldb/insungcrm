import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

import sys
sys.path.append('../..')
from isscm.models import Ordersheet, EstimateSheet
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404







def auto_db_update():

    or_month = get_object_or_404(Ordersheet, rp_date__lte=date.today() - relativedelta(day=3))
    es_month = get_object_or_404(EstimateSheet, no=or_month.essheet_pk)

    es_month.new_old = '기존'
    es_month.save()

    or_month.new_old = '기존'
    or_month.save()

auto_db_update()

