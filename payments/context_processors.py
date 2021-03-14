
from payments.models import IDCard, Transfer, Payment, Service, Balance

LATEST_LIMITS = 5

def payment_context(request):
    idcard = None
    balance = None
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
            
        if hasattr(request.user,'balance'):
            balance = request.user.balance

        

    context = {
        'idcard' : idcard,
        'balance' : balance,
        'has_idcard': has_idcard,
    }
    return context