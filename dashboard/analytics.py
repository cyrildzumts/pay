from pay import utils


def get_number_of_account():
    return utils.get_model('accounts', 'Account').objects.count()

def get_number_of_validated_account():
    return utils.get_model('accounts', 'Account').objects.filter(email_validated=True).count()

def get_number_of_active_account():
    return utils.get_model('accounts', 'Account').objects.filter(is_active=True).count()


def get_all_account_filter_by(**kwargs):
    return utils.get_model('accounts', 'Account').objects.filter(kwargs)

def get_account_filter_by(**kwargs):
    return utils.get_model('accounts', 'Account').objects.get(kwargs)


def get_number_of_account_filter_by(**kwars):
    return utils.get_model('accounts', 'Account').objects.filter(kwars).count()

def get_idcards_filter_by(**kwars):
    return utils.get_model('accounts', 'IDCard').objects.filter(kwars)

def get_nomber_of_idcards_filter_by(**kwars):
    return utils.get_model('accounts', 'IDCard').objects.filter(kwars).count()

def get_services_filter_by(**kwars):
    return utils.get_model('accounts', 'Service').objects.filter(kwars)

def get_number_of_services_filter_by(**kwars):
    return utils.get_model('accounts', 'Service').objects.filter(kwars).count()

def get_available_services_filter_by(**kwars):
    return utils.get_model('accounts', 'AvailableService').objects.filter(kwars)


def get_number_available_services_filter_by(**kwars):
    return utils.get_model('accounts', 'AvailableService').objects.filter(kwars).count()


def get_category_services_filter_by(**kwars):
    return utils.get_model('accounts', 'ServiceCategory').objects.filter(kwars)


def get_number_category_services_filter_by(**kwars):
    return utils.get_model('accounts', 'ServiceCategory').objects.filter(kwars).count()


def get_policies_filter_by(**kwars):
    return utils.get_model('accounts', 'Policy').objects.filter(kwars)


def get_number_of_policies_filter_by(**kwars):
    return utils.get_model('accounts', 'Policy').objects.filter(kwars).count()


def get_model_instance_filter_by(appName=None, modelName=None, **kwars):
    return utils.get_model(appName, modelName).objects.get(kwars)

def get_model_all_instance_filter_by(appName=None, modelName=None, **kwars):
    return utils.get_model(appName, modelName).objects.filter(kwars)

def get_number_model_instance_filter_by(appName=None, modelName=None, **kwars):
    return utils.get_model(appName, modelName).objects.filter(kwars).count()