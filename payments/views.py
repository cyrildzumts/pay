import json
from django.shortcuts import render
from accounts.models import Account
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.urls import reverse, resolve
from payments.payment_service import PaymentService
# from cart.models import Cart, CartItem
from pay import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#from order import checkout

# Create your views here.


@csrf_protect
@login_required
def show_payments(request):
    template_name = "paments/payments.html"
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
