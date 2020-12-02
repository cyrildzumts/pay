
from payments.models import IDCard, Transfer, Payment, Service, Balance

LATEST_LIMITS = 5

def payment_context(request):
    idcard = None
    has_idcard = False
    has_payments = False
    has_transfers = False
    has_services = False
    latest_payments = None
    latest_transfers = None
    latest_services = None
    if request.user.is_authenticated:
        try:
            idcard = IDCard.objects.get(user=request.user)
            has_idcard = True
            
        except IDCard.DoesNotExist:
            pass
        latest_payments = Payment.get_user_payments(request.user)[:LATEST_LIMITS]
        latest_transfers = Transfer.get_user_transfers(request.user)[:LATEST_LIMITS]
        latest_services = Service.get_user_services(request.user)[:LATEST_LIMITS]
        

    context = {
        'idcard' : idcard,
        'balance' : request.user.balance,
        'has_idcard': has_idcard,
        'latest_payments' : latest_payments,
        'latest_transfers' : latest_transfers,
        'latest_services' : latest_services
    }
    return context