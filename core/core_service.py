from django.db.models import F, Q, Count, Sum
from django.shortcuts import render
from django.contrib.auth.models import User
from django.template.loader import get_template, render_to_string
from django.contrib.staticfiles import finders
from voucher.models import Recharge, Voucher
from pay import settings
import os
import logging
import datetime
from xhtml2pdf import pisa


logger = logging.getLogger(__name__)

def generate_recharge_reports(template_name, output_name, seller=None):
    template_name = template_name or "report_content.html"
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(days=now.day-1, hours=now.hour, minutes=now.minute, seconds=now.second)
    end_delta = datetime.timedelta(days=1,hours=-23, minutes=-59, seconds=-59)
    end_date = datetime.datetime(now.year, now.month +1, 1) - end_delta
    user_seller =  None
    if isinstance(seller, str):
        try:
            user_seller = User.objects.get(username=seller)
            entry_list = Recharge.objects.filter(seller=user_seller,created_at__year=now.year, created_at__month=now.month)
        except User.DoesNotExist:
            logger.warn("report generator : no seller {seller} found")
            return
        #total = Recharge.objects.filter(created_at__year=now.year, created_at__month=now.month).aggregate(total=Sum('amount')).get('total') or 0
    elif isinstance(seller, User):
        user_seller = seller
        entry_list = Recharge.objects.filter(seller=seller,created_at__year=now.year, created_at__month=now.month)
    else:

        entry_list = Recharge.objects.filter(created_at__year=now.year, created_at__month=now.month)

    total = entry_list.aggregate(total=Sum('amount')).get('total') or 0
    
    context = {
        'SITE_NAME' : settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'CONTACT_MAIL': settings.CONTACT_MAIL,
        'DATE': now,
        'orientation' : 'portrait',
        'FRAME_NUMBER' : 2,
        'page_size': 'letter portrait',
        'border': '',
        'entry_list' : entry_list,
        'TOTAL' : total,
        'COUNT': entry_list.count(),
        'CURRENCY': settings.CURRENCY,
        'REPORT_TITLE' : _('Recharge Sumary'),
        'start_date': start_date,
        'end_date': end_date
    }
    report_html = render_to_string(template_name, context)
    report_pdf = open(output_name, 'w+b')
    pdf_status = pisa.CreatePDF(report_html, dest=report_pdf)
    report_pdf.close()
    if pdf_status.err:
        logger.error("error when creating the report pdf")
    else:
        logger.info("report pdf created")




def generate_sold_voucher_reports(template_name, output_name, seller=None):
    template_name = template_name or "sold_vouchers_report.html"
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(days=now.day-1, hours=now.hour, minutes=now.minute, seconds=now.second)
    end_delta = datetime.timedelta(days=1,hours=-23, minutes=-59, seconds=-59)
    end_date = datetime.datetime(now.year, now.month +1, 1) - end_delta
    user_seller =  None
    if isinstance(seller, str):
        try:
            user_seller = User.objects.get(username=seller)
            entry_list = Voucher.objects.filter(seller=user_seller,is_sold=True, sold_by=seller ,created_at__year=now.year, created_at__month=now.month)
        except User.DoesNotExist:
            logger.warn("report generator : no seller {seller} found")
            return
        #total = Recharge.objects.filter(created_at__year=now.year, created_at__month=now.month).aggregate(total=Sum('amount')).get('total') or 0
    elif isinstance(seller, User):
        user_seller = seller
        entry_list = Voucher.objects.filter(seller=user_seller,is_sold=True, sold_by=seller ,created_at__year=now.year, created_at__month=now.month)
    else:
        entry_list = Voucher.objects.filter(created_at__year=now.year, is_sold=True ,created_at__month=now.month)

    total = entry_list.aggregate(total=Sum('amount')).get('total') or 0
    
    context = {
        'SITE_NAME' : settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'CONTACT_MAIL': settings.CONTACT_MAIL,
        'DATE': now,
        'orientation' : 'portrait',
        'FRAME_NUMBER' : 2,
        'page_size': 'letter portrait',
        'border': '',
        'entry_list' : entry_list,
        'TOTAL' : total,
        'COUNT': entry_list.count(),
        'CURRENCY': settings.CURRENCY,
        'REPORT_TITLE' : _('Sold Voucher Card Sumary'),
        'start_date': start_date,
        'end_date': end_date
    }
    report_html = render_to_string(template_name, context)
    report_pdf = open(output_name, 'w+b')
    pdf_status = pisa.CreatePDF(report_html, dest=report_pdf)
    report_pdf.close()
    if pdf_status.err:
        logger.error("error when creating the report pdf")
    else: