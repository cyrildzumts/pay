from pay import settings
from django.contrib.auth.models import User
from voucher import voucher_service

def voucher_context(request):
    is_seller = False
    if request.user.is_authenticated:
        is_seller = request.user.groups.filter(name=settings.GROUP_SELLER).exists()
    
    context = {
        'is_seller' : is_seller
    }
    return context