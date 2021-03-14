
from payments.models import IDCard, Transfer, Payment, Service, Balance

RECENT_LIMIT = 8
REQUEST_PATH = ['/accounts/', '/payments/']

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
    activity_list = None
    if request.user.is_authenticated:
        try:
            idcard = IDCard.objects.get(user=request.user)
            has_idcard = True
            
        except IDCard.DoesNotExist:
            pass
            
        if hasattr(request.user,'balance'):
            balance = request.user.balance
            if request.path in REQUEST_PATH:
                activity_list = BalanceHistory.objects.filter(balance=balance).order_by('-created_at')[:RECENT_LIMIT]
        
        

    context = {
        'idcard' : idcard,
        'balance' : balance,
        'has_idcard': has_idcard,
        'activity_list': activity_list,
    }
    return context