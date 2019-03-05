def get_postdata(request):
    return request.POST.copy()


def get_session(request):
    return request.session

def get_data_from_request(request_dict, key):
    val = None
    if request_dict and key :
        val = request_dict[key]
    
    return val