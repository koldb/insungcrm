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
from datetime import date, timedelta
import datetime


def auto_db_update():
    or_month = Ordersheet.objects.filter(rp_date__lte=date.today() - relativedelta(months=3))
    or_month.update(new_old='기존')

    es_month = EstimateSheet.objects.filter(rp_date__lte=date.today() - relativedelta(months=3), finish="종료")
    es_month.update(new_old='기존')
    print("구분 업데이트 완료", datetime.datetime.now())


auto_db_update()
