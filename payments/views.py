import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.views.generic.dates import (
    YearArchiveView, MonthArchiveView, DayArchiveView, 
    DateDetailView, TodayArchiveView, ArchiveIndexView
)
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import F, Q
from accounts.models import Account
from payments.models import (
    Transaction, Transfer, AvailableService, Payment, 
    Service, ServiceCategory, Policy, CaseIssue, Reduction,
    IDCard
)
from payments.forms import (
    TransactionForm, TransferForm, ServiceCreationForm, 
    RechargeForm, IDCardForm, UpdateIDCardForm, PaymentForm,TransactionVerificationForm
)
from payments.payment_service import PaymentService, voucher_service
from pay import settings, utils
from pay.tasks import send_mail_task
import logging

logger = logging.getLogger(__name__)
#from order import checkout

# Create your views here.

## NOTE : Every views here query model that belongs to the user makink the request


@login_required
def payment_home(request):
    template_name = "payments/payment_home.html"
    page_title = _("Payment" + " - " + settings.SITE_NAME)    
    context = {
        'page_title' : page_title,
    }
    return render(request=request, template_name=template_name, context=context)

@csrf_protect
@login_required
def show_payments(request):
    template_name = "payments/payments.html"
    # checkout_url = checkout.get_checkout_url(request)
    #match = resolve('/payments/')


    return render(request=request, template_name=template_name)
# Create your views here.


@csrf_exempt
def ajax_make_payment(request):

    response = {}
    response['state'] = False
    return HttpResponse(json.dumps(response),
                        content_type="application/json")


# ajax cart update view.
@csrf_exempt
def ajax_validate_payment(request):
    """
    This method is called from JQuery.  it updates the Cart
    When 
    """
    response ={}
    response['state'] = False
    return HttpResponse(json.dumps(response),
                        content_type="application/json")

@login_required
def transactions(request):
    context = {}
    #current_account = Account.objects.get(user=request.user)
    #user_transactions = Transaction.objects.filter(Q(sender=request.user) | Q(recipient=request.user) )
    template_name = "payments/transactions_home.html"
    page_title = _("Transactions" + " - " + settings.SITE_NAME)
    context['page_title'] = page_title
    #context['transactions'] = user_transactions
    return render(request,template_name, context)


@login_required
def transaction_archive(request):
    context = {}
    #current_account = Account.objects.get(user=request.user)
    #user_transactions = Transaction.objects.filter(Q(sender=request.user) | Q(recipient=request.user) )
    template_name = "payments/transaction_archive.html"
    page_title = _("Transaction Archive" + " - " + settings.SITE_NAME)
    context['page_title'] = page_title
    #context['transactions'] = user_transactions
    return render(request,template_name, context)

@login_required
def new_transaction(request):
    """
    This view is responsible for processing transactions.
    To process a transaction : 
    The user must provide the following informations :
        * recipient ID
        * the amount of money to send
        * the type of transaction : TRANSFER, INVOICE PAYMENT, SERVICE CONSUMER
    For TRANSFER no more information data are needed.
    For INVOICE PAYMENT, the following extra informations are needed :
        * Invoice Reference Number
        * Invoice Date
        * Customer ID of as used by the recipient
    For SERVICE CONSUMER, the following extra informations are needed :
        The needed information are dependent of the type of service.
        A service REF ID is needed to identify the actual data needed.
    """
    context = {}
    email_template_name = "payments/transaction_done_email.html"
    template_name = "payments/new_transaction.html"
    page_title = "New Transaction" + " - " + settings.SITE_NAME
    logger.debug("New transaction request incoming")
    if request.method == "POST":
        context = PaymentService.process_transaction_request(request=request)
        if context['success']:
            redirect('payments:transaction-done')
        else : 
            logger.debug("There was an error with the transaction request : %s", context['errors'])

    elif request.method == "GET":
        
        context = {
                'page_title': page_title,
                'form': TransactionForm()
        }
    return render(request, template_name, context)


def transaction_done(request):
    
    context = {}
    template_name = "payments/transaction_done.html"
    page_title = _("Transaction Confirmation" + ' - ' + settings.SITE_NAME)
    context['page_title'] = page_title
    return render(request,template_name, context)


@login_required
def transaction_details(request, transaction_uuid=None):

    context = {}
    current_account = Account.objects.get(user=request.user)
    user_transactions = Transaction.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
    transaction = get_object_or_404(user_transactions, transaction_uuid=transaction_uuid)
    template_name = "payments/transaction_detail.html"
    page_title = _("Transaction Details" + " - " + settings.SITE_NAME)
    context['page_title'] = page_title
    context['transaction'] = transaction
    return render(request,template_name, context)



@login_required
def transfers(request):
    context = {}
    queryset = Transfer.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    template_name = "payments/transfer_list.html"
    page_title = _("My Transers" + " - " + settings.SITE_NAME)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['transfer_list'] = list_set
    return render(request,template_name, context)

@login_required
def new_transfer(request):
    """
    This view is responsible for processing a service.
    To process a transaction : 
    The user must provide the following informations :
        * recipient ID
        * the amount of money to send
        * the type of transaction : TRANSFER, INVOICE PAYMENT, SERVICE CONSUMER
    For TRANSFER no more information data are needed.
    
    """
    context = {}
    email_template_name = "payments/transfer_done_email.html"
    template_name = "payments/new_transfer.html"
    page_title = _("New Transfer" + " - " + settings.SITE_NAME)
    
    if request.method == "POST":
        context = PaymentService.process_transfer_request(request)
        if context['success']:
            return redirect('payments:transaction-done')
        else : 
            logger.error("There was an error with the transfer request")

    elif request.method == "GET":
            form = TransferForm()
            context = {
                'page_title':page_title,
                'form': form,
                'contacts': User.objects.filter(is_staff=False)
            }
    return render(request, template_name, context)

@login_required
def transfer_done(request):
    logger.info("Transfer Done")
    context = {}
    template_name = "payments/transfer_done.html"
    page_title = _("Transfer Confirmation" + " - " + settings.SITE_NAME)
    context['page_title'] = page_title
    return render(request,template_name, context)


@login_required
def transfer_details(request, transfer_uuid=None):
    context = {}
    transfer = None
    logger.info("transfer_detail() called with request.user = \"%s\" - transfer_uuid = \"%s\" ", request.user, transfer_uuid)
    try:
        transfer = Transfer.objects.get(Q(sender=request.user)|Q(recipient=request.user),transfer_uuid=transfer_uuid)
    except Transfer.DoesNotExist as e:
        logger.warning("user %s requested transfer with uuid %s not found", request.user, transfer_uuid)
        logger.exception(e)
        raise Http404('Transfer not found')
    template_name = "payments/transfer_detail.html"
    page_title = _("Transfer Details" + " - " + settings.SITE_NAME)
    context['page_title'] = page_title
    context['transfer'] = transfer
    return render(request,template_name, context)

@login_required
def services(request):
    context = {}
    queryset = Service.objects.select_related('category').filter(Q(customer=request.user) | Q(operator=request.user))
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    template_name = "payments/service_list.html"
    page_title = _("Services" + " - " + settings.SITE_NAME)
    context['page_title'] = page_title
    context['service_list'] = list_set
    return render(request,template_name, context)



@login_required
def transfer_verify(request):
    context = {}
    template_name = "payments/transfer_verify.html"
    page_title = _("Transfer Verification" + " + " + settings.SITE_NAME)
    if request.method == 'POST':
        form = TransactionVerificationForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data.get('verification_code')
            operator_reference = form.cleaned_data.get('operator_reference')
            flag , transfer = PaymentService.verify_transfer(user=request.user, verification_code=verification_code, operator_reference=operator_reference)
            context['transfer_is_valid'] = flag
            context['transfer_verification_ready'] = True
            
            if flag:
                context['transfer'] = transfer
                msg = "Transfer Verification successful. This transfer is valid"
                messages.success(request, _(msg))
                logger.info(msg)
            else :
                msg = "Transfer Verification failed. This transfer is not valid"
                messages.error(request, _(msg))
                logger.info(msg)

        else:
            context['transfer_is_valid'] = False
            context['transfer_verification_ready'] = False
            msg = "Form is invalid"
            messages.error(request, _(msg))
            logger.error(msg)
            logger.error(form.errors)
    elif request.method == 'GET':
        form = TransactionVerificationForm()
    context['page_title'] = page_title
    context['form'] = form
    return render(request,template_name, context)


@login_required
def new_service(request, available_service_uuid=None):
    '''
    This view is responsible for processing a service.
    To process a transaction service : 
    The user must provide the following informations :
        * recipient ID
        * the amount of money to send
        * Invoice Reference Number
        * Invoice Date
        * Customer ID of as used by the recipient
    For SERVICE CONSUMER, the following extra informations are needed :
        The needed information are dependent of the type of service.
        A service REF ID is needed to identify the actual data needed.
    '''
    context = {}
    email_template_name = "payments/service_done_email.html"
    template_name = "payments/new_service.html"
    page_title = _("Service Usage")
    if request.method == "POST":
        postdata = utils.get_postdata(request)
        commission = postdata.get('commission')
        if commission :
            postdata['commission'] = commission.replace(',', '.')
        form = ServiceCreationForm(postdata)
        if form.is_valid():
            customer = request.user
            seller = form.cleaned_data.get('operator')
            amount = form.cleaned_data.get('price')
            succeed = PaymentService.process_service(customer=customer, seller=seller, amount=amount, service_data=form.cleaned_data)
            if succeed:
                messages.success(request, _('We have send you a confirmation E-Mail. You will receive it in an instant'))
                logger.info("Service request successful. Redirecting now to service-done")
                return redirect('payments:transaction-done')
            else : 
                logger.error("There was an error with the service request ")
                service = get_object_or_404(AvailableService, available_uuid=available_service_uuid)
                commission = service.operator.policygroup_set.first().policy.commission
                context = {
                    'page_title':page_title,
                    'service' : service,
                    'commission' : commission,
                    'form': form
                }
        else:
            logger.error("Service Form is invalid : %s", form.errors)
            service = get_object_or_404(AvailableService, available_uuid=available_service_uuid)
            commission = service.operator.policygroup_set.first().policy.commission
            context = {
                'page_title':page_title,
                'service' : service,
                'commission' : commission,
                'form': form
            }

    elif request.method == "GET":
            form = ServiceCreationForm()
            service = get_object_or_404(AvailableService, available_uuid=available_service_uuid)
            commission = service.operator.policygroup_set.first().policy.commission
            context = {
                'page_title':page_title,
                'service' : service,
                'commission' : commission,
                'form': form
            }
    return render(request, template_name, context)


@login_required
def service_done(request):
    logger.info("Transfer Done")
    context = {}
    template_name = "payments/service_done.html"
    page_title = _("Service Payment Confirmation" + " - " + settings.SITE_NAME)
    context['page_title'] = page_title
    return render(request,template_name, context)

@login_required
def service_details(request, service_uuid=None):
    context = {}
    
    user_services = Service.objects.filter(Q(operator=request.user) | Q(customer=request.user) )
    service = get_object_or_404(user_services, service_uuid=service_uuid)
    template_name = "payments/service_detail.html"
    page_title = _("Service Details - " + settings.SITE_NAME)
    context['page_title'] = page_title
    context['service'] = service
    return render(request,template_name, context)


@login_required
def service_verify(request):
    context = {}
    template_name = "payments/service_verify.html"
    page_title = _("Service Verification" + " + " + settings.SITE_NAME)
    if request.method == 'POST':
        form = TransactionVerificationForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data.get('verification_code')
            operator_reference = form.cleaned_data.get('operator_reference')
            flag , service = PaymentService.verify_service(user=request.user, verification_code=verification_code, operator_reference=operator_reference)
            context['service_is_valid'] = flag
            context['service_verification_ready'] = True
            
            if flag:
                context['service'] = service
                msg = "Payment Verification successful. This payment is valid"
                messages.success(request, _(msg))
                logger.info(msg)
            else :
                msg = "Payment Verification failed. This payment is not valid"
                messages.error(request, _(msg))
                logger.info(msg)

        else:
            context['service_is_valid'] = False
            context['service_verification_ready'] = False
            msg = "Form is invalid"
            messages.error(request, _(msg))
            logger.error(msg)
            logger.error(form.errors)
    elif request.method == 'GET':
        form = TransactionVerificationForm()
    context['page_title'] = page_title
    context['form'] = form
    return render(request,template_name, context)


@login_required
def service_categories(request):
    context = {}
    categories = ServiceCategory.objects.filter(is_active=True)
    template_name = "payments/service_category_list.html"
    page_title = "Service Categories" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['category_list'] = categories
    return render(request,template_name, context)


@login_required
def service_category_details(request, category_uuid=None):
    context = {}
    category = get_object_or_404(ServiceCategory, category_uuid=category_uuid)
    template_name = "payments/service_category_detail.html"
    page_title = "Service Category Details" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['category'] = category
    return render(request,template_name, context)

@login_required
def available_services(request):
    context = {}
    queryset = AvailableService.objects.all()
    template_name = "payments/available_service_list.html"
    page_title = "Available Services - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['available_service_list'] = list_set
    return render(request,template_name, context)


@login_required
def available_service_details(request, available_uuid=None):
    context = {}
    service= get_object_or_404(AvailableService, available_uuid=available_uuid)
    template_name = "payments/available_service_detail.html"
    page_title = "Available Service Details" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['service'] = service
    return render(request,template_name, context)


@login_required
def new_payment(request):
    context = {}
    email_template_name = "payments/payment_done_email.html"
    template_name = "payments/new_payment.html"
    page_title = "Payment"
    if request.method == "POST":
        context = PaymentService.process_payment_request(request)
        if context['success']:
            messages.success(request, 'We have send you a confirmation E-Mail. You will receive it in an instant')
            """
            send_mail_task.apply_async(args=[context['email_context']],
                queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
                routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
            )
            """
            logger.info("Payment request successful")
            return redirect('payments:transaction-done')
        else : 
            logger.debug("There was an error with the service request : {}".format(context['errors']))
            form = PaymentForm(request.POST.copy())

    elif request.method == "GET":
            form = PaymentForm()
    context = {
        'page_title':page_title,
        'form': form
    }
    return render(request, template_name, context)

@login_required
def payment_done(request):
    logger.info("Payment Done")
    context = {}
    template_name = "payments/payment_done.html"
    page_title = "Payment Confirmation" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    return render(request,template_name, context)

@login_required
def payments(request):
    context = {}
    queryset = Payment.objects.filter(Q(sender=request.user) | Q(recipient=request.user) )
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    template_name = "payments/payment_list.html"
    page_title = "Payments" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['payment_list'] = list_set
    return render(request,template_name, context)

@login_required
def payments_year_archive(request, year):
    context = {}
    queryset = Payment.objects.filter(Q(sender=request.user) | Q(recipient=request.user) )
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    template_name = "payments/payment_list.html"
    page_title = "Payments" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['payment_list'] = list_set
    return render(request,template_name, context)

@login_required
def payments_month_archive(request, year, month):
    context = {}
    queryset = Payment.objects.filter(Q(sender=request.user) | Q(recipient=request.user) )
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    template_name = "payments/payment_list.html"
    page_title = "Payments" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['payment_list'] = list_set
    return render(request,template_name, context)

@login_required
def payments_day_archive(request, year, month, day):
    context = {}
    queryset = Payment.objects.filter(Q(sender=request.user) | Q(recipient=request.user) )
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    template_name = "payments/payment_list.html"
    page_title = "Payments" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['payment_list'] = list_set
    return render(request,template_name, context)

@login_required
def payment_details(request, payment_uuid=None):
    context = {}
    user_payments = Payment.objects.filter(Q(sender=request.user) | Q(recipient=request.user) )
    payment = get_object_or_404(user_payments, payment_uuid=payment_uuid)
    template_name = "payments/payment_details.html"
    page_title = "Payment Details" + " + " + settings.SITE_NAME
    context['page_title'] = page_title
    context['payment'] = payment
    return render(request,template_name, context)


@login_required
def payment_verify(request):
    context = {}
    template_name = "payments/payment_verify.html"
    page_title = "Payment Verification" + " + " + settings.SITE_NAME
    if request.method == 'POST':
        form = TransactionVerificationForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data.get('verification_code')
            operator_reference = form.cleaned_data.get('operator_reference')
            flag, payment = PaymentService.verify_payment(user=request.user, verification_code=verification_code, operator_reference=operator_reference)
            context['payment_is_valid'] = flag
            context['payment_verification_ready'] = True
            if flag:
                context['payment'] = payment
                msg = "Payment Verification successful. Verification code \"{}\" - Operator reference \"{}\" ".format(verification_code, operator_reference)
                messages.add_message(request=request, level=messages.SUCCESS, message=msg)
                logger.info(msg)
            else :
                msg = "Payment Verification failed. Verification code \"{}\" - Operator reference \"{}\" ".format(verification_code, operator_reference)
                messages.add_message(request=request, level=messages.ERROR, message=msg)
                logger.info(msg)

        else:
            context['payment_is_valid'] = False
            context['payment_verification_ready'] = False
            msg = "Form is invalid"
            messages.add_message(request=request, level=messages.ERROR, message=msg)
            logger.error(msg)
            logger.error(form.errors)
    elif request.method == 'GET':
        form = TransactionVerificationForm()
    context['page_title'] = page_title
    context['form'] = form
    return render(request,template_name, context)


@login_required
def policies(request):
    context = {}
    queryset = Policy.objects.all()
    template_name = "payments/policy_list.html"
    page_title = "Policies" + " + " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['policies'] = list_set
    return render(request,template_name, context)


@login_required
def policy_details(request, policy_uuid=None):
    context = {}
    policy = get_object_or_404(Policy, policy_uuid=policy_uuid)
    template_name = "payments/policy_detail.html"
    page_title = "Policy Details" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['policy'] = policy
    return render(request,template_name, context)

@login_required
def cases(request):
    context = {}
    queryset = CaseIssue.objects.filter(Q(participant_1=request.user) | Q(participant_2=request.user) )
    template_name = "payments/claim_list.html"
    page_title = "Claims" + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['claim_list'] = list_set
    return render(request,template_name, context)

@login_required
def case_details(request, issue_uuid=None):
    context = {}
    user_claims = CaseIssue.objects.filter(Q(participant_1=request.user) | Q(participant_2=request.user))
    claim = get_object_or_404(user_claims, issue_uuid=issue_uuid)
    template_name = "payments/claim_detail.html"
    page_title = "Claim Details"+ " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['claim'] = claim
    return render(request,template_name, context)

@login_required
def reductions(request):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Reduction')
    current_reductions = model.objects.all()
    template_name = "payments/reduction_list.html"
    page_title = "Reductions" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['reductions'] = current_reductions
    return render(request,template_name, context)


@login_required
def reduction_details(request, reduction_uuid=None):
    context = {} 
    reduction = get_object_or_404(Reduction, reduction_uuid=reduction_uuid)
    template_name = "payments/reduction_detail.html"
    page_title = "Reduction Details" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['reduction'] = reduction
    return render(request,template_name, context)



@login_required
def recharge(request):
    '''
    This view is responsible for recharging the user balance.
    To process a recharge : 
    The user must provide the following informations :
        * voucher code ( string)
    
    '''
    email_template_name = "payments/recharge_done_email.html"
    template_name = "payments/recharge.html"
    page_title = _("Account Recharge")
    context = {
        'page_title':page_title
    }
    if request.method == "POST":
        postdata = utils.get_postdata(request)
        recharge_form = RechargeForm(postdata)
        if recharge_form.is_valid():
            voucher = recharge_form.cleaned_data['voucher']
            succeed, amount = voucher_service.VoucherService.use_voucher(voucher, request.user.pk)
            if succeed:
                Account.objects.filter(user__username=settings.PAY_RECHARGE_USER).update(balance=F('balance') + amount)
                email_context = {
                    'title' : _('Recharge Confirmation'),
                    'customer_name': request.user.get_full_name(),
                    'voucher': voucher,
                    'amount' : amount,
                    'recipient_email': request.user.email,
                    'template_name': "accounts/account_recharge_done_email.html"
                }
                msg = 'Your account has been recharged.We have send you a confirmation E-Mail. You will receive an E-Mail in an instant'
                messages.success(request, _(msg))
                #send_mail_task.apply_async(args=[email_context],
                #    queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
                #    routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
                #)
                logger.info("Recharge was succefull")
                return redirect('accounts:account')
            else :
                messages.error(request, _("Voucher couldn't be used"))
                logger.error("Error : Recharge failed")
                context['form'] = recharge_form
            
        else : 
            logger.error("Form invalid: {}".format(context['errors']))
            context['form'] = recharge_form

    elif request.method == "GET":
            context['form'] = RechargeForm()
    return render(request, template_name, context)

@login_required
def idcards(request):
    context = {}
    queryset = IDCard.objects.filter(user=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    template_name = "payments/idcard_list.html"
    page_title = "ID Cards" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['idcards'] = list_set
    return render(request,template_name, context)


@login_required
def idcard_details(request, idcard_uuid=None):
    context = {}
    idcard = None
    try:
        idcard = IDCard.objects.get(user=request.user, idcard_uuid=idcard_uuid)
    except IDCard.DoesNotExist as e:
        logger.exception(e)
        raise Http404('IDCard not found')

    template_name = "payments/idcard_detail.html"
    page_title = "My ID Card" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['idcard'] = idcard
    return render(request,template_name, context)



@login_required
def upload_idcard(request):
    context = {}    
    template_name = "payments/upload_idcard.html"
    page_title = "Identification Solution" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    
    if request.method == "POST":
        postdata = utils.get_postdata(request)
        
        form = IDCardForm(postdata, request.FILES)
        if form.is_valid():
            logger.info("submitted idcard form is valide")
            post_user = form.cleaned_data.get('user')
            if post_user.pk == request.user.pk:
                logger.info("saving submitted idcard form")
                form.save()
                logger.info("submitted idcard form saved")
                return redirect('payments:upload-idcard-done')
            else :
                logger.warning("User uploading ID card suspicious : submitted user %s is different than the request user %s ", post_user.username, request.user.username )
        else:
            logger.error("The idcard form is not valide. Error : %s", form.non_field_errors)
    else:
        form = IDCardForm()
    context['form'] = form
    return render(request,template_name, context)


@login_required
def update_idcard(request, idcard_uuid=None):
    page_title = "Edit my account" + ' - ' + settings.SITE_NAME
    idcard = None
    try:
        idcard = IDCard.objects.get(user=request.user, idcard_uuid=idcard_uuid)
    except IDCard.DoesNotExist as e:
        logger.exception(e)
        raise Http404('IDCard not found')

    template_name = "payments/idcard_update.html"
    if request.method =="POST":
        form = UpdateIDCardForm(request.POST, request.FILES, instance=idcard)
        if form.is_valid():
            logger.info("Update IDCard form is valid")
            form.save()
            return redirect('accounts:account')
        else:
            logger.info("Edit Account form is not valid. Errors : %s", form.errors)
            logger.info("Form clean data : %s", form.cleaned_data)
    elif request.method == 'GET':
        form = UpdateIDCardForm(instance=idcard)
    context = {
            'page_title': page_title,
            'template_name': template_name,
            'idcard'  : idcard,
            'form': form
        }
    
    return render(request, template_name,context )


@login_required
def upload_idcard_done(request):
    context = {}
    template_name = "payments/upload_idcard_done.html"
    page_title = "ID Card uploaded" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    return render(request,template_name, context)



@login_required
def transaction_verification(request):
    context = {}
    template_name = "payments/transaction_verification.html"
    page_title = _("Transaction Verification" + " - " + settings.SITE_NAME)
    context['page_title'] = page_title
    return render(request,template_name, context)




class PaymentYearArchiveView(YearArchiveView):
    queryset = Payment.objects.all()
    date_field = "created_at"
    make_object_list = True
    paginated_by = utils.PAGINATED_BY
    def get_queryset(self):
        return Payment.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Payment Year Archive")
        return context


class PaymentMonthArchiveView(MonthArchiveView):
    queryset = Payment.objects.all()
    date_field = "created_at"
    make_object_list = True
    paginated_by = utils.PAGINATED_BY
    def get_queryset(self):
        return Payment.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Payment Month Archive")
        return context

class PaymentDayArchiveView(DayArchiveView):
    queryset = Payment.objects.all()
    date_field = "created_at"
    make_object_list = True
    paginated_by = utils.PAGINATED_BY
    def get_queryset(self):
        return Payment.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Payment Day Archive")
        return context


class PaymentTodayArchiveView(TodayArchiveView):
    queryset = Payment.objects.all()
    date_field = "created_at"
    make_object_list = True
    paginated_by = utils.PAGINATED_BY

    def get_queryset(self):
        return Payment.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Payment Archive from Today")
        return context



@method_decorator(login_required, name='dispatch')
class TransferArchiveIndexView(ArchiveIndexView):
    date_field = "created_at"
    make_object_list = True
    paginated_by = utils.PAGINATED_BY

    def get_queryset(self):
        return Transfer.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Transfer Archive")
        return context

@method_decorator(login_required, name='dispatch')
class TransferYearArchiveView(YearArchiveView):
    date_field = "created_at"
    make_object_list = True
    paginated_by = utils.PAGINATED_BY

    def get_queryset(self):
        return Transfer.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Transfer Year Archive")
        return context


@method_decorator(login_required, name='dispatch')
class TransferMonthArchiveView(MonthArchiveView):
    date_field = "created_at"
    make_object_list = True
    paginated_by = utils.PAGINATED_BY

    def get_queryset(self):
        return Transfer.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Transfer Month Archive")
        return context


@method_decorator(login_required, name='dispatch')
class TransferDayArchiveView(DayArchiveView):
    queryset = Transfer.objects.all()
    date_field = "created_at"
    make_object_list = True
    paginated_by = utils.PAGINATED_BY

    def get_queryset(self):
        return Transfer.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Transfer Day Archive")
        return context


@method_decorator(login_required, name='dispatch')
class TransferTodayArchiveView(TodayArchiveView):
    queryset = Transfer.objects.all()
    date_field = "created_at"
    make_object_list = True
    paginated_by = utils.PAGINATED_BY

    def get_queryset(self):
        return Transfer.objects.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Transfer Archive of Today")
        return context