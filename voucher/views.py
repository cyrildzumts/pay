from django.shortcuts import render
from django.views.generic import ListView, DetailView
from voucher.models import Voucher, SoldVoucher, UsedVoucher, Recharge
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from pay import settings, utils
from voucher.forms import VoucherCreationForm, RechargeCustomerAccount, RechargeCustomerAccountByStaff
from voucher.tasks import generate_voucher
from voucher import voucher_service
from django.utils.translation import gettext as _
import logging
from datetime import datetime
# Create your views here.

logger = logging.getLogger(__name__)


@login_required
def voucher_home(request):
    context = {}
    #model = utils.get_model('voucher', 'Voucher')
    # TODO Must be fixed : The users visiting this must have the appropiatre
    # permission
    template_name = "voucher/voucher.html"
    page_title = _("Voucher Dashboard") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    messages.info(request, _("Welcome back to voucher page"))
    return render(request, template_name, context)


@login_required
def vouchers(request):
    context = {}
    #model = utils.get_model('voucher', 'Voucher')
    # TODO Must be fixed : The users visiting this must have the appropiatre
    # permission
    vouchers = Voucher.objects.order_by('pk').all()
    template_name = "voucher/voucher_list.html"
    page_title = _("Voucher List") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['vouchers'] = vouchers
    return render(request, template_name, context)


@login_required
def voucher_details(request, pk=None):
    page_title = _("Voucher Details") + ' | ' + settings.SITE_NAME
    instance = get_object_or_404(Voucher, pk=pk)
    template_name = "voucher/voucher_details.html"

    context = {
        'page_title': page_title,
        'site_name': settings.SITE_NAME,
        'template_name': template_name,
        'voucher': instance
    }
    return render(request, template_name, context)


@login_required
def voucher_activate(request, pk=None):
    c = Voucher.objects.filter(pk=pk, activated=False, is_used=False).update(
        activated=True, activated_at=datetime.now(), activated_by=request.user)
    if c > 0:
        return redirect('voucher:vouchers')
    else:
        return redirect('voucher:voucher_details', pk=pk)


@login_required
def recharge_user_account_view(request):
    #TODO : Add permission check here if must be check if the user sending this request 
    # is allowed to recharge a user account
    page_title = _("Recharge User Account") + ' | ' + settings.SITE_NAME
    template_name = "voucher/recharge.html"
    context = {}
    logger.info("User Recharge Account view requested by user %s", request.user.get_full_name())
    if request.method == "POST":
        logger.info("Received new Recharge request for user account")
        postdata = utils.get_postdata(request)
        form = RechargeCustomerAccountByStaff(postdata)
        if form.is_valid():
            seller = form.cleaned_data['seller']
            customer = form.cleaned_data['customer']
            amount = form.cleaned_data['amount']
            logger.info("recharge_user_account_view() : Received form is valid. Customer = %s - Seller = %s - Amount = %s .", customer, seller, amount)
            customer = get_object_or_404(User, pk=customer)
            seller = get_object_or_404(User, pk=seller)
            result = voucher_service.VoucherService.process_recharge_user_account(seller=seller, customer=customer, amount=amount)
            if result.get('succeed', False):
                messages.success(request, _("The customer account has been successfuly recharged"))
                context['succeed'] = True
                logger.info("recharge_user_account_view() : Customer %s was successfully recharge with the Amount = %s .", customer, amount)
            else :
                messages.error(request, _("Your request could not processed. You might need to check that the submitted data are correct."))
                context['succeed'] = True
                logger.info("recharge_user_account_view() : Customer = %s could not be recharge with the  Amount = %s .", customer, amount)
        else :
            
            context['errors'] = _("The submitted form is not valid. Verify the form fields")
            context['form'] = form
            messages.error(request, _("The submitted form is not valid. Verify the form fields"))
            logger.info("recharge_user_account_view() : Received form is invalid")
            logger.error(form.errors)
    elif request.method == "GET":
        form = RechargeCustomerAccountByStaff()
        context['form'] = form,
    return render(request,template_name, context)
    

"""
@login_required
def sell_voucher_view(request):
    logger.debug('Sell_voucher_view called')
    postdata = utils.get_postdata(request)
    request_type = postdata.get('type', "")
    if request_type == "ACTIVATE":
        pk = int(postdata.get('pk', -1))
        if pk > 0:
            now = datetime.now()
            c = Voucher.objects.filter(pk=pk, activated=False, is_used=False).update(activated=True,
                                                                                     activated_at=now, activated_by=request.user, is_sold=True, sold_at=now, sold_by=request.user)
            SoldVoucher.objects.create(voucher=pk, seller=request.user)
    elif request_type == "RECHARGE_STAFF":
        form = RechargeCustomerAccountByStaff(postdata)
        if form.is_valid:
            seller = form.cleaned_data['seller']
            customer = form.cleaned_data['customer']
            amount = form.cleaned_data['amount']
            recharge_by = form.cleaned_data['recharge_by']
"""

@login_required
def used_vouchers(request):
    context = {}
    #model = utils.get_model('voucher', 'Voucher')
    # TODO Must be fixed : The users visiting this must have the appropiatre
    # permission
    used_vouchers = UsedVoucher.objects.all()
    template_name = "voucher/used_voucher_list.html"
    page_title = _("Used Voucher List") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['used_vouchers'] = used_vouchers
    return render(request, template_name, context)


@login_required
def used_voucher_details(request, pk=None):
    page_title = _("Used Voucher Details") + ' | ' + settings.SITE_NAME
    instance = get_object_or_404(UsedVoucher, pk=pk)
    template_name = "voucher/used_voucher_details.html"
    context = {
        'page_title': page_title,
        'site_name': settings.SITE_NAME,
        'template_name': template_name,
        'used_voucher': instance
    }
    return render(request, template_name, context)


@login_required
def sold_vouchers(request):
    context = {}
    #model = utils.get_model('voucher', 'Voucher')
    # TODO Must be fixed : The users visiting this must have the appropiatre
    # permission
    sold_vouchers = SoldVoucher.objects.all()
    template_name = "voucher/sold_voucher_list.html"
    page_title = _("Sold Voucher List") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['sold_vouchers'] = sold_vouchers
    return render(request, template_name, context)


@login_required
def sold_voucher_details(request, pk=None):
    page_title = _("Sold Voucher Details") + ' | ' + settings.SITE_NAME
    instance = get_object_or_404(SoldVoucher, pk=pk)
    template_name = "voucher/sold_voucher_details.html"
    context = {
        'page_title': page_title,
        'site_name': settings.SITE_NAME,
        'template_name': template_name,
        'sold_voucher': instance
    }
    return render(request, template_name, context)


@login_required
def voucher_generate(request):
    page_title = _("Voucher Generator") + ' | ' + settings.SITE_NAME
    template_name = "voucher/voucher_generate.html"
    if request.method == "POST":
        postdata = utils.get_postdata(request)
        form = VoucherCreationForm(postdata)
        if form.is_valid():
            name = form.cleaned_data['name']
            amount = form.cleaned_data['amount']
            number = form.cleaned_data['number']
            logger.info("Submitted Voucher Creation Form is valid.")
            logger.info(
                "Voucher creation request : Name : %s - Amout : %s - Number : %s", name, amount, number)
            generate_voucher.apply_async(
                args=[{
                    'name': name,
                    'amount': amount,
                    'number': number
                }],
                queue=settings.CELERY_VOUCHER_GENERATE_QUEUE,
                routing_key=settings.CELERY_VOUCHER_ROUTING_KEY
            )
            logger.info("Voucher Creation pushed in the Queue")
            return redirect('voucher:voucher_home')
    context = {
        'page_title': page_title,
        'site_name': settings.SITE_NAME,
        'template_name': template_name,
    }
    return render(request, template_name, context)


class RechargeView(ListView):
    queryset = Recharge.objects.order_by('-created_at')
    context_object_name = "recharge_list"
    template_name = 'voucher/recharge_list.html'

class RechargeDetailView(DetailView):
    queryset = Recharge.objects.all()
    context_object_name = "recharge"
    template_name = 'tags/recharge_details.html'