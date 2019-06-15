
from django.apps import apps

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