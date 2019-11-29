from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.models import User, Group, Permission
from django.db.models import F, Q
from rest_framework.authtoken.models import Token
from pay import utils, settings
from dashboard import forms
from dashboard import analytics
import logging
from pay.tasks import send_mail_task


logger = logging.getLogger(__name__)
# Create your views here.


@login_required
def dashboard(request):
    template_name = "dashboard/dashboard.html"
    allowed =request.user.is_superuser or request.user.groups.filter(Q(name='Administration') or Q(name='Manager') or Q(name='Marketing')).exists()
    logger.debug("Dashboard Current User Groups Logs :", request.user.groups.all())
    page_title = _('Dashboard') + '| ' + settings.SITE_NAME
    username = request.user.username
    if not allowed :
        context = {
        'name'          : username,
        'page_title'    : page_title,
        'is_allowed'     : allowed
        }  
        logger.warning("Access Denied : A user %s with no appropriate permission has requested the Dashboard Page", username)
    else : 
        context = {
            'name'          : username,
            'page_title'    : page_title,
            'summary' : analytics.dashboard_summary(),
            'recent_transfers' : analytics.get_recent_transfers(),
            'recent_services' : analytics.get_recent_services(),
            'is_allowed'     : allowed
        }
        logger.info("Authorized Access : User %s has requested the Dashboard Page", username)

    return render(request, template_name, context)


@login_required
def generate_token(request):
    allowed = request.user.groups.filter(Q(name='Administration') or Q(name='Manager') or Q(name='Marketing')).exists()
    template_name = "dashboard/token_generate.html"
    context = {
        'page_title' :_('User Token Generation') + ' - ' + settings.SITE_NAME,
        'is_allowed' : allowed,
    }
    
    if allowed:
        if request.method == 'POST':
            form = forms.TokenForm(utils.get_postdata(request))
            if form.is_valid():
                user_id = form.cleaned_data['user']
                username = form.cleaned_data['username']
                user = User.objects.get(pk=user_id)
                t = Token.objects.get_or_create(user=user)
                context['generated_token'] = t
                messages.add_message(request, messages.SUCCESS, _('Token successfully generated for user {}'.format(username)) )
                return redirect('dashboard:home')
            else :
                messages.add_message(request, messages.ERROR, _('The submitted form is not valid') )
        else :
            context['form'] = forms.TokenForm()

    return render(request, template_name, context)
        
    

@login_required
def service_details(request, service_uuid=None):
    context = {}
    model = utils.get_model('payments', 'Service')
    user_services = model.objects.filter(Q(operator=request.user) | Q(customer=request.user) )
    service = get_object_or_404(user_services, service_uuid=service_uuid)
    template_name = "dashboard/service_detail.html"
    page_title = "Service Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['service'] = service
    context['service_summary'] = analytics.get_service_usage_summary()
    return render(request,template_name, context)


@login_required
def services(request):
    context = {}
    model = utils.get_model('payments', 'Service')
    services = model.objects.select_related('category').all()
    template_name = "dashboard/service_list.html"
    page_title = _("Dashboard Services") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['services'] = services
    context['service_summary'] = analytics.get_service_usage_summary()
    return render(request,template_name, context)



@login_required
def available_services(request):
    context = {}
    model = utils.get_model('payments', 'AvailableService')
    available_services = model.objects.all()
    template_name = "dashboard/available_service_list.html"
    page_title = "Available Services - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['available_services'] = available_services
    return render(request,template_name, context)

def available_service_update(request, available_uuid=None):
    page_title = _("Edit Available Service")+ ' | ' + settings.SITE_NAME
    instance = get_object_or_404(forms.AvailableService, available_uuid=available_uuid)
    template_name = "dashboard/available_service_update.html"
    if request.method =="POST":
        form = forms.AvailableServiceForm(request.POST, instance=instance)
        if form.is_valid():
            logger.info("AvailableServiceForm for instance %s is valid", form.cleaned_data['name'])
            form.save()
            return redirect('dashboard:available_services')
        else:
            logger.info("Edit AvailableServiceForm is not valid. Errors : %s", form.errors)
    
    form = forms.AvailableServiceForm(instance=instance)
    categories = analytics.get_categories()
    operators = analytics.get_operators()
    context = {
            'page_title':page_title,
            'template_name':template_name,
            'service' : instance,
            'form': form,
            'categories': categories,
            'operators': operators
        }
    
    return render(request, template_name,context )

@login_required
def available_service_create(request):
    page_title = _("Create Available Service")+ ' | ' + settings.SITE_NAME
    template_name = "dashboard/available_service_create.html"
    form = None
    if request.method =="POST":
        form = forms.AvailableServiceForm(request.POST)
        if form.is_valid():
            logger.info("AvailableServiceForm for instance %s is valid", form.cleaned_data['name'])
            form.save()
            return redirect('dashboard:available_services')
        else:
            form = forms.AvailableServiceForm()
            logger.info("Edit AvailableServiceForm is not valid. Errors : %s", form.errors)
    elif request.method == "GET":
        form = forms.AvailableServiceForm()
        categories = analytics.get_categories()
        operators = analytics.get_operators()

    context = {
            'page_title':page_title,
            'template_name':template_name,
            'form': form,
            'categories': categories,
            'operators': operators
        }
    
    
    return render(request, template_name,context )

@login_required
def available_service_remove(request, available_uuid=None):
    page_title = _("Edit Available Service")+ ' | ' + settings.SITE_NAME
    template_name = "dashboard/available_service_remove.html"
    if request.method =="POST":
        form = forms.AvailableServiceForm(request.POST)
        if form.is_valid() and forms.AvailableService.objects.filter(available_uuid=available_uuid).exists() :
            forms.AvailableService.objects.filter(available_uuid=available_uuid).delete()
            logger.info("AvailableServiceForm for instance %s is valid", form.cleaned_data['name'])
            return redirect('dashboard:available_services')
        else:
            logger.info("Edit AvailableServiceForm is not valid. Errors : %s", form.errors)
    
    instance = get_object_or_404(forms.AvailableService, pk=pk)
    form = forms.AvailableServiceForm(instance=instance)
    context = {
            'page_title':page_title,
            'template_name':template_name,
            'service' : instance,
            'form': form
        }
    
    return render(request, template_name,context )

@login_required
def available_service_details(request, available_uuid=None):
    context = {}
    model = utils.get_model('payments', 'AvailableService')
    service= get_object_or_404(model, available_uuid=available_uuid)
    template_name = "dashboard/available_service_detail.html"
    page_title = "Available Service Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['service'] = service
    return render(request,template_name, context)

@login_required
def category_services(request):
    context = {}
    model = utils.get_model('payments', 'ServiceCategory')
    categories = model.objects.filter()
    template_name = "dashboard/category_service_list.html"
    page_title = "Service Categories - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['categories'] = categories
    return render(request,template_name, context)


@login_required
def category_service_update(request, category_uuid=None):
    page_title = _("Edit Category Service")+ ' | ' + settings.SITE_NAME
    instance = get_object_or_404(forms.ServiceCategory, category_uuid=category_uuid)
    template_name = "dashboard/category_service_update.html"
    if request.method =="POST":
        form = forms.ServiceCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            logger.info("ServiceCategoryForm for instance %s is valid", form.cleaned_data['category_name'])
            form.save()
            return redirect('dashboard:category_services')
        else:
            logger.info("Edit ServiceCategoryForm is not valid. Errors : %s", form.errors)
    
    form = forms.ServiceCategoryForm(instance=instance)
    context = {
            'page_title':page_title,
            'template_name':template_name,
            'category' : instance,
            'form': form
        }
    
    return render(request, template_name,context )


@login_required
def category_service_remove(request, category_uuid=None):
    page_title = _("Removing Category Service")+ ' | ' + settings.SITE_NAME
    template_name = "dashboard/category_service_remove.html"
    if request.method =="POST":
        form = forms.ServiceCategoryForm(request.POST)
        if form.is_valid() and forms.ServiceCategory.objects.filter(category_uuid=category_uuid).exists() :
            forms.ServiceCategory.objects.filter(category_uuid=category_uuid).delete()
            logger.info("ServiceCategoryForm for instance %s is valid", form.cleaned_data['category_name'])
            return redirect('dashboard:category_services')
        else:
            logger.info("Edit ServiceCategoryForm is not valid. Errors : %s", form.errors)
    
    instance = get_object_or_404(forms.AvailableService, category_uuid=category_uuid)
    form = forms.AvailableServiceForm(instance=instance)
    context = {
            'page_title':page_title,
            'template_name':template_name,
            'category' : instance,
            'form': form
        }
    
    return render(request, template_name,context )


@login_required
def category_service_create(request):
    page_title = _("Create Category Service")+ ' | ' + settings.SITE_NAME
    template_name = "dashboard/category_service_create.html"
    form = None
    if request.method =="POST":
        form = forms.ServiceCategoryForm(request.POST)
        if form.is_valid():
            logger.info("ServiceCategoryForm for instance %s is valid", form.cleaned_data['category_name'])
            form.save()
            return redirect('dashboard:category_services')
        else:
            form = forms.ServiceCategoryForm()
            logger.info("Edit ServiceCategoryForm is not valid. Errors : %s", form.errors)
    elif request.method == "GET":
        form = forms.ServiceCategoryForm()

    context = {
            'page_title':page_title,
            'template_name':template_name,
            'form': form
        }
    
    
    return render(request, template_name,context )


@login_required
def category_service_details(request, category_uuid=None):
    context = {}
    model = utils.get_model('payments', 'ServiceCategory')
    avs_model = utils.get_model('payments', 'AvailableService')
    category = get_object_or_404(model, category_uuid=category_uuid)
    avs = avs_model.objects.filter(category=category)
    template_name = "dashboard/category_service_detail.html"
    page_title = "Service Category Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['category'] = category
    context['has_services'] = category.available_services.exists()
    context['available_services'] = category.available_services.all()
    return render(request,template_name, context)


@login_required
def policies(request):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Policy')
    #current_account = Account.objects.get(user=request.user)
    current_policies = model.objects.all()
    template_name = "dashboard/policy_list.html"
    page_title = "Policies - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['policies'] = current_policies
    return render(request,template_name, context)


@login_required
def policy_update(request, policy_uuid=None):
    page_title = _("Edit Policy")+ ' | ' + settings.SITE_NAME
    instance = get_object_or_404(forms.Policy, policy_uuid=policy_uuid)
    template_name = "dashboard/policy_update.html"
    if request.method =="POST":
        form = forms.PolicyForm(request.POST, instance=instance)
        if form.is_valid():
            logger.info("PolicyForm for instance %s is valid", form.cleaned_data['commission'])
            form.save()
            return redirect('dashboard:policies')
        else:
            logger.info("Edit PolicyForm is not valid. Errors : %s", form.errors)
    
    form = forms.PolicyForm(instance=instance)
    context = {
            'page_title':page_title,
            'template_name':template_name,
            'policy' : instance,
            'form': form
        }
    
    return render(request, template_name,context )



@login_required
def policy_remove(request, policy_uuid=None):
    page_title = _("Removing Policy")+ ' | ' + settings.SITE_NAME
    template_name = "dashboard/policy_remove.html"
    if request.method =="POST":
        form = forms.PolicyForm(request.POST)
        if form.is_valid() and forms.Policy.objects.filter(policy_uuid=policy_uuid).exists() :
            forms.Policy.objects.filter(policy_uuid=policy_uuid).delete()
            logger.info("PolicyForm for instance %s is valid", form.cleaned_data['commission'])
            return redirect('dashboard:policies')
        else:
            logger.info("Edit PolicyForm is not valid. Errors : %s", form.errors)
    
    instance = get_object_or_404(forms.Policy, policy_uuid=policy_uuid)
    form = forms.PolicyForm(instance=instance)
    context = {
            'page_title':page_title,
            'template_name':template_name,
            'policy' : instance,
            'form': form
        }
    
    return render(request, template_name,context )



@login_required
def policy_create(request):
    page_title = _("Create Policy")+ ' | ' + settings.SITE_NAME
    template_name = "dashboard/policy_create.html"
    form = None
    if request.method =="POST":
        form = forms.PolicyForm(request.POST)
        if form.is_valid():
            logger.info("PolicyForm for instance %s is valid", form.cleaned_data['commission'])
            form.save()
            return redirect('dashboard:policies')
        else:
            form = forms.PolicyForm()
            logger.info("Edit ServiceCategoryForm is not valid. Errors : %s", form.errors)
    elif request.method == "GET":
        form = forms.PolicyForm()

    context = {
            'page_title':page_title,
            'template_name':template_name,
            'form': form
        }
    
    
    return render(request, template_name,context )


@login_required
def policy_details(request, policy_uuid=None):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Policy')
    #current_account = Account.objects.get(user=request.user)
    policy = get_object_or_404(model, policy_uuid=policy_uuid)
    template_name = "dashboard/policy_detail.html"
    page_title = "Policy Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['policy'] = policy
    return render(request,template_name, context)





@login_required
def transfers(request):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Transfer')
    #current_account = Account.objects.get(user=request.user)
    queryset = model.objects.all()
    template_name = "dashboard/transfer_list.html"
    page_title = "Transfers - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['transfers'] = queryset
    return render(request,template_name, context)


@login_required
def transfer_details(request, transfer_uuid=None):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Transfer')
    transfer = get_object_or_404(model, transfer_uuid=transfer_uuid)
    template_name = "dashboard/transfer_detail.html"
    page_title = "Transfer Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['transfer'] = transfer
    return render(request,template_name, context)

@login_required
def payments(request):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Payment')
    #current_account = Account.objects.get(user=request.user)
    queryset = model.objects.all()
    template_name = "dashboard/payment_list.html"
    page_title = "Payments - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['payments'] = queryset
    return render(request,template_name, context)


@login_required
def payment_details(request, payment_uuid=None):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Payment')
    payment = get_object_or_404(model, payment_uuid=payment_uuid)
    template_name = "dashboard/payment_detail.html"
    page_title = "Payment Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['payment'] = payment
    return render(request,template_name, context)

@login_required
def cases(request):
    context = {}
    model = utils.get_model(app_name='payments', modelName='CaseIssue')
    #current_account = Account.objects.get(user=request.user)
    queryset = model.objects.all()
    template_name = "dashboard/cases.html"
    page_title = "Cases - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['cases'] = queryset
    return render(request,template_name, context)


@login_required
def case_details(request, issue_uuid=None):
    context = {}
    model = utils.get_model(app_name='payments', modelName='CaseIssue')
    claim = get_object_or_404(model, issue_uuid=issue_uuid)
    template_name = "dashboard/case_detail.html"
    page_title = "Claim Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['claim'] = claim
    return render(request,template_name, context)



@login_required
def case_close(request, issue_uuid=None):
    context = {}
    model = utils.get_model(app_name='payments', modelName='CaseIssue')
    claim = get_object_or_404(model, issue_uuid=issue_uuid)
    template_name = "dashboard/case_close.html"
    page_title = "Claim Closing - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['claim'] = claim
    return render(request,template_name, context)


@login_required
def usage(request):
    pass


@login_required
def model_usage(request, appName=None, modelName=None):
    pass


@login_required
def groups(request):
    context = {}
    
    #current_account = Account.objects.get(user=request.user)
    group_list = Group.objects.all()
    template_name = "dashboard/group_list.html"
    page_title = "Groups" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['groups'] = group_list
    return render(request,template_name, context)

@login_required
def group_detail(request, pk=None):
    context = {}
    group = get_object_or_404(Group, pk=pk)
    template_name = "dashboard/group_detail.html"
    page_title = "Group Detail" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['group'] = group
    return render(request,template_name, context)


@login_required
def group_create(request):
    context = None
    page_title = 'Group Creation'
    template_name = 'dashboard/group_create.html'
    form = forms.GroupFormCreation()
    if request.method == 'POST':
        form = forms.GroupFormCreation(request.POST)
        users = request.POST.getlist('users')
        if form.is_valid() and users:
            logger.debug("Group Create : Form is Valid")
            group = form.save()
            group.user_set.set(users)
            logger.debug("Added users into the group %s",users)
            return redirect('dashboard:groups')
        else :
            logger.error("Error on adding  users %s into the group",users)
    
    context = {
            'page_title' : page_title,
            'form': form,
            'users' : User.objects.all(),
            'permissions': Permission.objects.all()
    }
    return render(request, template_name, context)