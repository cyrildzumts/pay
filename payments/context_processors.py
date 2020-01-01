
from payments.models import IDCard

def payment_context(request):
    idcard = None
    has_idcard = False
    if request.user.is_authenticated:
        try:
            idcard = IDCard.objects.get(user=request.user)
            has_idcard = True
        except IDCard.DoesNotExist:
            pass

    context = {
        'idcard' : idcard,
        'has_idcard': has_idcard
    }
    return context