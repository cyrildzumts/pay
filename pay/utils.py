
from django.apps import apps
import secrets

def get_postdata(request):
    return request.POST.copy()


def get_session(request):
    return request.session

def get_data_from_request(request_dict, key):
    val = None
    if request_dict and key :
        val = request_dict[key]
    
    return val

    
def get_model(app_name=None, modelName=None):
    model = None
    if app_name and modelName:
        try:
            model = apps.get_model(app_name, modelName)
        except LookupError as e:
            pass

    return model

def get_all_fields_from_form(instance):
    """"
    Return names of all available fields from given Form instance.

    :arg instance: Form instance
    :returns list of field names
    :return type: list
    """

    fields = list(instance().base_fields)

    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields

def generate_token_10():
    return secrets.token_urlsafe(10)