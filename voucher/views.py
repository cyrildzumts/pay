from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import User
from django.db.models import F, Q
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from pay import settings, utils, conf
from voucher.forms import VoucherCreationForm, RechargeCustomerAccount, RechargeCustomerAccountByStaff
from voucher.tasks import generate_voucher
from voucher import voucher_service
from voucher.models import Voucher, SoldVoucher, UsedVoucher, Recharge
from django.utils.translation import gettext_lazy as _
from voucher.resources import ui_strings
from django.utils import timezone
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
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)
    template_name = "voucher/voucher.html"
    page_title = _("Voucher Dashboard") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['recharge_list'] = voucher_service.VoucherService.get_recharge_set(seller=request.user)[:conf.RECENT_LIMIT]
    messages.info(request, _("Welcome back to voucher page"))
    return render(request, template_name, context)


@login_required
def vouchers(request):
    context = {}
    #model = utils.get_model('voucher', 'Voucher')
    # TODO Must be fixed : The users visiting this must have the appropiatre
    # permission
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)
    template_name = "voucher/voucher_list.html"
    page_title = _("Voucher List") + " - " + settings.SITE_NAME
    

    voucher_list = voucher_service.VoucherService.get_voucher_set(created_by=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(voucher_list, conf.PAGINATED_BY)
    try:
        voucher_set = paginator.page(page)
    except PageNotAnInteger:
        voucher_set = paginator.page(1)
    except EmptyPage:
        voucher_set = None
    context['voucher_list'] = voucher_set
    context['page_title'] = page_title
    
    return render(request, template_name, context)


@login_required
def voucher_details(request, voucher_uuid=None):
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)
    page_title = _("Voucher Details") + ' | ' + settings.SITE_NAME
    template_name = "voucher/voucher_details.html"
    context = {
        'page_title': page_title,
        'voucher' : get_object_or_404(Voucher, voucher_uuid=voucher_uuid)
    }

    return render(request, template_name, context)


@login_required
def voucher_activate(request, voucher_uuid=None):
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)

    c = Voucher.objects.filter(voucher_uuid=voucher_uuid, activated=False, is_used=False).update(
        activated=True, activated_at=timezone.now(), activated_by=request.user, is_sold=True, sold_by=request.user, sold_at=timezone.now())
    if c > 0:
        messages.success(request, _("Voucher activated"))
        return redirect('voucher:vouchers')
    else:
        messages.error(request, _("Voucher not activated"))
        return redirect('voucher:voucher-detail', voucher_uuid=voucher_uuid)



@login_required
def recharge_user_account_view(request):

    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)

    page_title = _("Recharge User Account") + ' - ' + settings.SITE_NAME
    template_name = "voucher/recharge.html"
    
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
            #result = voucher_service.VoucherService.process_recharge_user_account(seller=seller, customer=customer, amount=amount)
            result = voucher_service.VoucherService.recharge_balance(seller=seller, customer=customer, amount=amount)
            if result.get('succeed', False):
                messages.success(request, _("The customer balance has been successfully recharged"))
                logger.info("recharge_user_account_view() : Customer %s was successfully recharge with the Amount = %s .", customer, amount)
                return redirect('voucher:voucher-home')
            else :
                messages.error(request, _("Your request could not processed. You might need to check that the submitted data are correct."))
                logger.info("recharge_user_account_view() : Customer = %s could not be recharge with the  Amount = %s .", customer, amount)
        else :
            
            context['errors'] = _("The submitted form is not valid. Verify the form fields")
            context['form'] = form
            messages.error(request, _("The submitted form is not valid. Verify the form fields"))
            logger.info("recharge_user_account_view() : Received form is invalid")
            logger.error(form.errors)
    elif request.method == "GET":
        form = RechargeCustomerAccountByStaff()
    context = {
        'form' : form,
        'page_title' : page_title
    }
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
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)
    context = {}
    #model = utils.get_model('voucher', 'Voucher')
    # TODO Must be fixed : The users visiting this must have the appropiatre
    # permission
    voucher_list = Voucher.objects.filter(is_used=True, sold_by=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(voucher_list, 10)
    try:
        voucher_set = paginator.page(page)
    except PageNotAnInteger:
        voucher_set = paginator.page(1)
    except EmptyPage:
        voucher_set = None
    template_name = "voucher/used_voucher_list.html"
    page_title = _("Used Voucher List") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['voucher_list'] = voucher_set
    return render(request, template_name, context)


@login_required
def used_voucher_details(request, voucher_uuid=None):
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)
    page_title = _("Used Voucher Details") + ' | ' + settings.SITE_NAME
    instance = get_object_or_404(UsedVoucher, voucher_uuid=voucher_uuid)
    template_name = "voucher/voucher_details.html"
    context = {
        'page_title': page_title,
        'used_voucher': instance,
        'voucher' : instance
    }
    return render(request, template_name, context)


@login_required
def sold_vouchers(request):
    context = {}
    #model = utils.get_model('voucher', 'Voucher')
    # TODO Must be fixed : The users visiting this must have the appropiatre
    # permission
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)

    voucher_list = Voucher.objects.filter(Q(is_sold=True)|Q(activated=True), sold_by=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(voucher_list, 10)
    try:
        voucher_set = paginator.page(page)
    except PageNotAnInteger:
        voucher_set = paginator.page(1)
    except EmptyPage:
        voucher_set = None
    template_name = "voucher/sold_voucher_list.html"
    page_title = _("Sold Voucher List") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['voucher_list'] = voucher_set
    return render(request, template_name, context)


@login_required
def sold_voucher_details(request, voucher_uuid=None):
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)
    page_title = _("Sold Voucher Details") + ' | ' + settings.SITE_NAME
    instance = get_object_or_404(Voucher, voucher_uuid=voucher_uuid)
    template_name = "voucher/voucher_details.html"
    context = {
        'page_title': page_title,
        'sold_voucher': instance,
        'voucher' : instance
    }
    return render(request, template_name, context)


@login_required
def voucher_generate(request):
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)
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
            logger.info(f"Voucher creation request by user {request.user.username} : Name : {name} - Amout : {amount} - Number : {number}")
            generate_voucher.apply_async(
                args=[{
                    'name': name,
                    'amount': amount,
                    'number': number,
                    'user': request.user.pk
                }],
                queue=settings.CELERY_VOUCHER_GENERATE_QUEUE,
                routing_key=settings.CELERY_VOUCHER_ROUTING_KEY
            )
            logger.info("Voucher Creation pushed in the Queue")
            return redirect('voucher:voucher-home')
    context = {
        'page_title': page_title,
        'template_name': template_name,
    }
    return render(request, template_name, context)



@login_required
def recharges(request):
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)
    context = {}
    #model = utils.get_model('voucher', 'Voucher')
    # TODO Must be fixed : The users visiting this must have the appropiatre
    # permission
    recharge_list = voucher_service.VoucherService.get_recharge_set(seller=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(recharge_list, 10)
    try:
        voucher_set = paginator.page(page)
    except PageNotAnInteger:
        voucher_set = paginator.page(1)
    except EmptyPage:
        voucher_set = None
    template_name = "voucher/recharge_list.html"
    page_title = _("Recharge List") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['recharge_list'] = recharge_list
    return render(request, template_name, context)


@login_required
def recharge_details(request, recharge_uuid=None):
    is_seller = voucher_service.is_seller(request.user)
    if not is_seller:
        raise SuspiciousOperation(ui_strings.UI_PAGE_NOT_ALLOWED)
    page_title = _("Recharge Info") + ' | ' + settings.SITE_NAME
    instance = get_object_or_404(Recharge, recharge_uuid=recharge_uuid)
    template_name = "voucher/recharge_details.html"
    context = {
        'page_title': page_title,
        'template_name': template_name,
        'recharge': instance,
        'voucher': instance.voucher
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