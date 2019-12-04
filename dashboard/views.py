from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    queryset = model.objects.select_related('category').all()
    template_name = "dashboard/service_list.html"
    page_title = _("Dashboard Services") + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['services'] = list_set
    context['service_summary'] = analytics.get_service_usage_summary()
    return render(request,template_name, context)



@login_required
def available_services(request):
    context = {}
    model = utils.get_model('payments', 'AvailableService')
    queryset = model.objects.all()
    template_name = "dashboard/available_service_list.html"
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
    context['available_services'] = list_set
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
            return redirect('dashboard:available-services')
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
            avs = form.save()
            forms.AvailableService.objects.filter(pk=avs.pk).update(created_by=request.user)
            return redirect('dashboard:available-services')
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
    # TODO Check if the user requesting the deletion has the permission
    deleted_count, extras = forms.AvailableService.objects.filter(available_uuid=available_uuid).delete()
    if deleted_count > 0 :
        messages.add_message(request, messages.SUCCESS, 'AvailableService has been deleted')
        logger.debug("AvailableService deleted by User {}", request.user.username)
    
    else:
        messages.add_message(request, messages.ERROR, 'AvailableService could not be deleted')
        logger.error("AvailableService Delete failed. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:available-services')
    
@login_required
def available_service_remove_all(request):
    # TODO Check if the user requesting the deletion has the permission
    deleted_count, extras = forms.AvailableService.objects.all().delete()
    if deleted_count > 0 :
        messages.add_message(request, messages.SUCCESS, 'All AvailableService has been deleted')
        logger.debug("All AvailableService deleted by User {}", request.user.username)
    
    else:
        messages.add_message(request, messages.ERROR, 'All AvailableService could not be deleted')
        logger.error("All AvailableService Delete failed. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:home')

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
    queryset = model.objects.all()
    template_name = "dashboard/category_service_list.html"
    page_title = "Service Categories - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['categories'] = list_set
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
            return redirect('dashboard:category-services')
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
    # TODO Check if the user requesting the deletion has the permission
    deleted_count, extras = forms.ServiceCategory.objects.filter(category_uuid=category_uuid).delete()
    if deleted_count > 0 :
        messages.add_message(request, messages.SUCCESS, 'Service Category has been deleted')
        logger.debug("Service Category deleted by User {}", request.user.username)
    
    else:
        messages.add_message(request, messages.ERROR, 'Service Category could not be deleted')
        logger.error("Service Category Delete failed. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:category-services')


@login_required
def category_service_remove_all(request):
    # TODO Check if the user requesting the deletion has the permission
    deleted_count, extras = forms.ServiceCategory.objects.all().delete()
    if deleted_count > 0 :
        messages.add_message(request, messages.SUCCESS, 'All ServiceCategory has been deleted')
        logger.debug("All ServiceCategory deleted by User {}", request.user.username)
    
    else:
        messages.add_message(request, messages.ERROR, 'All ServiceCategory could not be deleted')
        logger.error("All ServiceCategory Delete failed. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:home')


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
            return redirect('dashboard:category-services')
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
    queryset = model.objects.all()
    template_name = "dashboard/policy_list.html"
    page_title = "Policies - " + settings.SITE_NAME
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
    # TODO Check if the user requesting the deletion has the permission
    deleted_count, extras = forms.Policy.objects.filter(policy_uuid=policy_uuid).delete()
    if deleted_count > 0 :
        messages.add_message(request, messages.SUCCESS, 'Policy has been deleted')
        logger.debug("Policy deleted by User {}", request.user.username)
    
    else:
        messages.add_message(request, messages.ERROR, 'Policy could not be deleted')
        logger.error("Policy Delete failed. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:policies')


@login_required
def policy_remove_all(request):
    # TODO Check if the user requesting the deletion has the permission
    deleted_count, extras = forms.Policy.objects.all().delete()
    if deleted_count > 0 :
        messages.add_message(request, messages.SUCCESS, 'All Policies has been deleted')
        logger.debug("All Policies deleted by User {}", request.user.username)
    
    else:
        messages.add_message(request, messages.ERROR, 'All Policies could not be deleted')
        logger.error("All Policies Delete failed. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:home')

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
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['transfers'] = list_set
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
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        payment_set = paginator.page(page)
    except PageNotAnInteger:
        payment_set = paginator.page(1)
    except EmptyPage:
        payment_set = None
    context['page_title'] = page_title
    context['payments'] = payment_set
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
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['cases'] = list_set
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
    page = request.GET.get('page', 1)
    paginator = Paginator(group_list, 10)
    try:
        group_set = paginator.page(page)
    except PageNotAnInteger:
        group_set = paginator.page(1)
    except EmptyPage:
        group_set = None
    context['page_title'] = page_title
    context['groups'] = group_set
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
def group_update(request, pk=None):
    # TODO CHECK if the requesting User has the permission to update a group
    context = None
    page_title = 'Group Update'
    template_name = 'dashboard/group_update.html'
    group = get_object_or_404(Group, pk=pk)
    form = forms.GroupFormCreation(instance=group)
    group_users = group.user_set.all()
    available_users = User.objects.exclude(pk__in=group_users.values_list('pk'))
    permissions = group.permissions.all()
    available_permissions = Permission.objects.exclude(pk__in=permissions.values_list('pk'))
    if request.method == 'POST':
        form = forms.GroupFormCreation(request.POST, instance=group)
        users = request.POST.getlist('users')
        if form.is_valid() :
            logger.debug("Group form for update is valid")
            if form.has_changed():
                logger.debug("Group has changed")
            group = form.save()
            if users:
                logger.debug("adding %s users [%s] into the group", len(users), users)
                group.user_set.set(users)
            logger.debug("Saved users into the group %s",users)
            return redirect('dashboard:groups')
        else :
            logger.error("Error on editing the group. The form is invalid")
    
    context = {
            'page_title' : page_title,
            'form': form,
            'group': group,
            'users' : group_users,
            'available_users' : available_users,
            'permissions': permissions,
            'available_permissions' : available_permissions
    }
    return render(request, template_name, context)


@login_required
def group_create(request):
    context = None
    page_title = 'Group Creation'
    template_name = 'dashboard/group_create.html'
    available_permissions = Permission.objects.all()
    available_users = User.objects.all()
    form = forms.GroupFormCreation()
    if request.method == 'POST':
        form = forms.GroupFormCreation(request.POST)
        users = request.POST.getlist('users')
        if form.is_valid():
            logger.debug("Group Create : Form is Valid")
            group_name = form.cleaned_data.get('name', None)
            logger.debug('Creating a Group with the name {}'.format(group_name))
            if not Group.objects.filter(name=group_name).exists():
                group = form.save()
                messages.add_message(request, messages.SUCCESS, "The Group has been succesfully created")
                if users:
                    group.user_set.set(users)
                    logger.debug("Added users into the group %s",users)
                else :
                    logger.debug("Group %s created without users", group_name)

                return redirect('dashboard:groups')
            else:
                msg = "A Group with the given name {} already exists".format(group_name)
                messages.add_message(request, messages.ERROR, msg)
                logger.error(msg)
            
        else :
            messages.add_message(request, messages.ERROR, "The Group could not be created. Please correct the form")
            logger.error("Error on creating new Group Errors : %s", form.errors)
    
    context = {
            'page_title' : page_title,
            'form': form,
            'available_users' : available_users,
            'available_permissions': available_permissions
    }
    return render(request, template_name, context)


@login_required
def group_delete(request, pk=None):
    # TODO Check if the user requesting the deletion has the Group Delete permission
    try:
        group = Group.objects.get(pk=pk)
        name = group.name
        messages.add_message(request, messages.SUCCESS, 'Group {} has been deleted'.format(name))
        group.delete()
        logger.debug("Group {} deleted by User {}", name, request.user.username)
        
    except Group.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Group could not be found. Group not deleted')
        logger.error("Group Delete : Group not found. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:groups')


#######################################################
########            Permissions 

@login_required
def permissions(request):
    context = {}
    permission_list = Permission.objects.all()
    template_name = "dashboard/permission_list.html"
    page_title = "Permissions" + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(permission_list, 10)
    try:
        permission_set = paginator.page(page)
    except PageNotAnInteger:
        permission_set = paginator.page(1)
    except EmptyPage:
        permission_set = None
    context['page_title'] = page_title
    context['permissions'] = permission_set
    return render(request,template_name, context)

@login_required
def permission_detail(request, pk=None):
    context = {}
    permission = get_object_or_404(Permission, pk=pk)
    template_name = "dashboard/permission_detail.html"
    page_title = "Permission Detail" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['permission'] = permission
    return render(request,template_name, context)


@login_required
def permission_update(request, pk=None):
    # TODO CHECK if the requesting User has the permission to update a permission
    context = None
    page_title = 'Permission Update'
    template_name = 'dashboard/permission_update.html'
    permission = get_object_or_404(Permission, pk=pk)
    form = forms.GroupFormCreation(instance=permission)
    permission_users = permission.user_set.all()
    available_users = User.objects.exclude(pk__in=permission_users.values_list('pk'))

    if request.method == 'POST':
        form = forms.GroupFormCreation(request.POST, instance=permission)
        users = request.POST.getlist('users')
        if form.is_valid() :
            logger.debug("Permission form for update is valid")
            if form.has_changed():
                logger.debug("Permission has changed")
            permission = form.save()
            if users:
                logger.debug("adding %s users [%s] into the permission", len(users), users)
                permission.user_set.set(users)
            logger.debug("Added permissions to users %s",users)
            return redirect('dashboard:permissions')
        else :
            logger.error("Error on editing the perssion. The form is invalid")
    
    context = {
            'page_title' : page_title,
            'form': form,
            'users' : permission_users,
            'available_users' : available_users,
            'permission': permission,
    }
    return render(request, template_name, context)


@login_required
def permission_create(request):
    context = None
    page_title = 'Permission Creation'
    template_name = 'dashboard/permission_create.html'
    available_groups = Group.objects.all()
    available_users = User.objects.all()
    form = forms.GroupFormCreation()
    if request.method == 'POST':
        form = forms.GroupFormCreation(request.POST)
        users = request.POST.getlist('users')
        if form.is_valid():
            logger.debug("Permission Create : Form is Valid")
            perm_name = form.cleaned_data.get('name', None)
            perm_codename = form.cleaned_data.get('codename', None)
            logger.debug('Creating a Permission with the name {}'.format(perm_name))
            if not Permission.objects.filter(Q(name=perm_name) | Q(codename=perm_codename)).exists():
                perm = form.save()
                messages.add_message(request, messages.SUCCESS, "The Permission has been succesfully created")
                if users:
                    perm.user_set.set(users)
                    logger.debug("Permission %s given to users  %s",perm_name, users)
                else :
                    logger.debug("Permission %s created without users", perm_name)

                return redirect('dashboard:permissions')
            else:
                msg = "A Permission with the given name {} already exists".format(perm_name)
                messages.add_message(request, messages.ERROR, msg)
                logger.error(msg)
            
        else :
            messages.add_message(request, messages.ERROR, "The Permission could not be created. Please correct the form")
            logger.error("Error on creating new Permission : %s", form.errors)
    
    context = {
            'page_title' : page_title,
            'form': form,
            'available_users' : available_users,
            'available_groups': available_groups
    }
    return render(request, template_name, context)


@login_required
def permission_delete(request, pk=None):
    # TODO Check if the user requesting the deletion has the Group Delete permission
    try:
        perm = Permission.objects.get(pk=pk)
        name = perm.name
        messages.add_message(request, messages.SUCCESS, 'Permission {} has been deleted'.format(name))
        perm.delete()
        logger.debug("Permission {} deleted by User {}", name, request.user.username)
        
    except Permission.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission could not be found. Permission not deleted')
        logger.error("Permission Delete : Permission not found. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:permissions')