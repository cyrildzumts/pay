
from payments.models import IDCard, Transfer, Payment, Service

LATEST_LIMITS = 5

def payment_context(request):
    idcard = None
    has_idcard = False
    has_payments = False
    has_transfers = False
    has_services = False
    if request.user.is_authenticated:
        try:
            idcard = IDCard.objects.get(user=request.user)
            has_idcard = True
        except IDCard.DoesNotExist:
            pass
        

    context = {
        'idcard' : idcard,
        'has_idcard': has_idcard,
        'latest_payments' : Payment.get_user_payments(request.user)[:LATEST_LIMITS],
        'latest_transfers' : Transfer.get_user_transfers(request.user)[:LATEST_LIMITS],
        'latest_services' : Service.get_user_services(request.user)[:LATEST_LIMITS]
    }
    return context