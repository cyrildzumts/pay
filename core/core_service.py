from django.db.models import F, Q, Count, Sum
from django.shortcuts import render
from django.contrib.auth.models import User
from django.template.loader import get_template, render_to_string
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles import finders
from voucher.models import Recharge, Voucher
from dashboard import analytics
from pay import settings
from payments.templatetags import payments_tags
from payments import constants as PAYMENTS_CONSTANTS
import os
import logging
import datetime
import io
from xhtml2pdf import pisa


logger = logging.getLogger(__name__)
PAYMENTS_ACTIVITIES = [PAYMENTS_CONSTANTS.BALANCE_ACTIVITY_SERVICE, PAYMENTS_CONSTANTS.BALANCE_ACTIVITY_PAYMENT, PAYMENTS_CONSTANTS.BALANCE_ACTIVITY_REFUND]

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
        logger.info("recharge report pdf created")




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
            logger.warn("report generator generate_sold_voucher_reports : no seller {seller} found")
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
        'entry_list' : entry_list.order_by('-sold_at'),
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
        logger.info("sold voucher report pdf created")



def generate_invoice(debug=False, output_name=None, user=None, date=datetime.date.today()):
    
    #start_date = now - datetime.timedelta(days=now.day-1, hours=now.hour, minutes=now.minute, seconds=now.second)
    #end_delta = datetime.timedelta(days=1,hours=-23, minutes=-59, seconds=-59)
    #end_date = datetime.datetime(now.year, now.month +1, 1) - end_delta
    #user_seller =  None
    if not isinstance(user, User):
        logger.warn("generate_invoice : no valid order")
        return None

    template_name = "reports/activities_invoice.html"
    filters = {
    #    'activity': activity,
        'balance' : user.balance,
        'created_at__year': date.year,
        'created_at__month': date.month
    }
    activities, details = analytics.detailed_activities_reports(**filters)
    activity_str = 'Activities'
    invoice_title = f"Invoice-Activities-{activity_str}-{user.get_full_name()}-{now.year}-{now.month}"
    context = {
        'SITE_NAME' : settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'CONTACT_MAIL': settings.CONTACT_MAIL,
        'DATE': now,
        'orientation' : 'portrait',
        'FRAME_NUMBER' : 2,
        'page_size': 'letter portrait',
        'border': debug,
        'entry_list' : activities,
        'TOTAL' : details.get('total', 0),
        'COUNT': details.get('count', 0),
        'CURRENCY': settings.CURRENCY,
        'INVOICE_TITLE' : f"Invoice-Activities-{now.year}-{now.month}",
        'ACTIVITY_NAME': activity_str
    }
    output_name = output_name or f"{invoice_title}.pdf"
    invoice_html = render_to_string(template_name, context)
    invoice_file = io.BytesIO()
    pdf_status = pisa.CreatePDF(invoice_html, dest=invoice_file, debug=False)
    if pdf_status.err:
        logger.error("error when creating the report pdf")
        return None
    else:
        logger.info("recharge report pdf created")
    return invoice_file


def report_payments(user,year, month, debug=False, output_name=None):
    #start_date = now - datetime.timedelta(days=now.day-1, hours=now.hour, minutes=now.minute, seconds=now.second)
    #end_delta = datetime.timedelta(days=1,hours=-23, minutes=-59, seconds=-59)
    #end_date = datetime.datetime(now.year, now.month +1, 1) - end_delta
    #user_seller =  None
    now = datetime.datetime.now()
    if not isinstance(user, User):
        logger.warn("generate_invoice : no valid order")
        return None
    if not isinstance(year, int) or year < 0 or year > now.year:
        logger.warn(f"generate_invoice : invalid year format. submitted year : {year}")
        return None
    if not isinstance(month, int) or month < 0 or month > 12:
        logger.warn(f"generate_invoice : invalid month format. submitted month : {month}")
        return None
    if year == now.year and month > now.month:
        logger.warn(f"generate_invoice : invalid date format. submitted year : {year} - month : {month}")
        return None

    template_name = "invoices/payment_reports.html"
    filters = {
        'activity__in': PAYMENTS_ACTIVITIES,
        'balance' : user.balance,
        'created_at__year': year,
        'created_at__month': month
    }
    activities, details = analytics.detailed_activities_reports(**filters)
    activity_str = payments_tags.balance_activity(PAYMENTS_CONSTANTS.BALANCE_ACTIVITY_PAYMENT)
    invoice_title = f"Invoice-Activities-{activity_str}-{user.get_full_name()}-{now.year}-{now.month}"
    context = {
        'SITE_NAME' : settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'CONTACT_MAIL': settings.CONTACT_MAIL,
        'DATE': now,
        'orientation' : 'portrait',
        'FRAME_NUMBER' : 2,
        'page_size': 'letter portrait',
        'border': debug,
        'entry_list' : activities,
        'TOTAL' : details.get('total', 0),
        'COUNT': details.get('count', 0),
        'CURRENCY': settings.CURRENCY,
        'INVOICE_TITLE' : invoice_title,
        'ACTIVITY_NAME': activity_str
    }
    output_name = output_name or f"{invoice_title}.pdf"
    invoice_html = render_to_string(template_name, context)
    invoice_file = io.BytesIO()
    pdf_status = pisa.CreatePDF(invoice_html, dest=invoice_file, debug=False)
    if pdf_status.err:
        logger.error("error when creating the report pdf")
        return None
    else:
        logger.info("recharge report pdf created")
    return invoice_file
