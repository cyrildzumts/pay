from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.db.models import F, Q
from pay import utils, settings
# Create your views here.



def dashboard(request):
    pass


def service_details(request, pk=None):
    context = {}
    model = utils.get_model('accounts', 'Service')
    user_services = model.objects.filter(Q(operator=request.user) | Q(customer=request.user) )
    service = get_object_or_404(user_services, pk=pk)
    template_name = "dashboard/service_details.html"
    page_title = "Service Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['service'] = service
    return render(request,template_name, context)

@login_required
def services(request):
    context = {}
    model = utils.get_model('accounts', 'Service')
    services = model.objects.select_related('category').all()
    template_name = "dashboard/service_list.html"
    page_title = _("Dashboard Services") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['services'] = services
    return render(request,template_name, context)

@login_required
def available_services(request):
    context = {}
    model = utils.get_model('accounts', 'AvailableService')
    available_services = model.objects.all()
    template_name = "dashboard/available_service_list.html"
    page_title = "Available Services - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['available_services'] = available_services
    return render(request,template_name, context)

def available_service_update(request, pk=None):
    pass

@login_required
def available_service_create(request):
    pass

@login_required
def available_service_remove(request, pk=None):
    pass

@login_required
def available_service_details(request, pk=None):
    context = {}
    model = utils.get_model('accounts', 'AvailableService')
    service= get_object_or_404(model, pk=pk)
    template_name = "dashboard/available_service_details.html"
    page_title = "Available Service Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['service'] = service
    return render(request,template_name, context)

@login_required
def category_services(request):
    context = {}
    model = utils.get_model('accounts', 'ServiceCategory')
    categories = model.objects.filter(is_active=True)
    template_name = "dashboard/service_category_list.html"
    page_title = "Service Categories - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['categories'] = categories
    return render(request,template_name, context)


@login_required
def category_service_update(request, pk=None):
    pass


@login_required
def category_service_remove(request, pk=None):
    pass


@login_required
def category_service_create(request):
    pass


@login_required
def category_service_details(request, pk=None):
    context = {}
    model = utils.get_model('accounts', 'ServiceCategory')
    category = get_object_or_404(model, pk=pk)
    template_name = "dashboard/service_category_details.html"
    page_title = "Service Category Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['category'] = category
    return render(request,template_name, context)


@login_required
def policies(request):
    context = {}
    model = utils.get_model(app_name='accounts', modelName='Policy')
    #current_account = Account.objects.get(user=request.user)
    current_policies = model.objects.all()
    template_name = "dashboard/policy_list.html"
    page_title = "Policies - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['policies'] = current_policies
    return render(request,template_name, context)


@login_required
def policy_update(request, pk=None):
    pass



@login_required
def policy_remove(request, pk=None):
    pass



@login_required
def policy_create(request):
    pass


@login_required
def policy_details(request, pk=None):
    context = {}
    model = utils.get_model(app_name='accounts', modelName='Policy')
    #current_account = Account.objects.get(user=request.user)
    policy = get_object_or_404(model, pk=pk)
    template_name = "dashboard/policy_details.html"
    page_title = "Policy Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['policy'] = policy
    return render(request,template_name, context)
