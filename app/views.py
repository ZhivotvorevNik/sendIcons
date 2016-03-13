from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import time
import user_agents
from .models import Service


def index(request):
    services = Service.objects.order_by('name')

    data = {
        'services': services
    }
    return render(request, 'index.html', data, context_instance=RequestContext(request))

def add(request):

    params = request.GET
    meta = request.META
    services = Service.objects.order_by('name')

    data = {
        'services': services
    }
    return render(request, 'add.html', data, context_instance=RequestContext(request))

# def index(request):
#
#     params = request.GET
#     meta = request.META
#     st = 'HELLO, '
#     date = time.strftime('%H:%M, %d %B %Y' ,time.localtime(time.time()))
#     data = {
#         'MESSAGE': st,
#         'USER': 'nizhi',
#         'ONLINE': False,
#         'dates': ['123', '324324', '324324', '32432432', '565465', '546546'],
#         'PARAMS': params,
#         'DATE': date,
#         'req': params,
#         'metas': meta
#     }
#     return render(request, 'index.html', data, context_instance=RequestContext(request))

def test(request):
    params = request.POST
    files = request.FILES
    cookies = request.COOKIES
    meta = request.META
    useragent = request.META.get('HTTP_USER_AGENT')
    result = user_agents.parse(useragent)
    isTouch = result.is_touch_capable

    services = Service.objects.order_by('name')

    uploadFile = files['file']

    print(files)
    print(files['file'].size)
    print(files['file'].content_type)
    print(files['file'].charset)
    print(files['file'].read())


    handle_uploaded_file(uploadFile )

    print(result.browser)
    data = {
        'params': params,
        'services': services,
        'COOKIES': cookies,
        'imgSrc': uploadFile.name,
        'META': meta,
        'useragent': result
    }
    return render(request, 'test.html', data)
    # return HttpResponse("Do something")

def handle_uploaded_file(file):
    with open('app/static/' + file.name, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)