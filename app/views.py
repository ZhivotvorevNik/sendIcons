# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
import os
import re
from subprocess import Popen, PIPE
import json
import user_agents
from .models import Service


def index(request):
    services = Service.objects.order_by('name')

    data = {
        'services': services
    }
    return render(request, 'index.html', data, context_instance=RequestContext(request))

def add(request):
    params = request.POST
    files = request.FILES
    data = {'status': 'error'}

    print(params)

    if 'file' in files:
        uploadFile = files['file']
        allowTypes = ['image/png', 'image/svg+xml']

        if uploadFile.content_type in allowTypes:
            handle_uploaded_file(uploadFile)
            data = {
                'status': 'ok',
                'imgSrc': uploadFile.name
            }

        else:
            data = {
                'status': 'error'
            }


    response = json.dumps(data)

    return HttpResponse(response)


def status(request):
    params = request.POST
    files = request.FILES
    cookies = request.COOKIES
    meta = request.META
    useragent = request.META.get('HTTP_USER_AGENT')
    result = user_agents.parse(useragent)
    isTouch = result.is_touch_capable
    data = {}

    services = Service.objects.order_by('name')

    os.chdir('morda')
    resp, err = Popen('git status', shell=True, stdout=PIPE).communicate()
    resp = str(resp, 'utf8')

    os.chdir('../')


    changeTemplate = re.compile('\t.*\n')
    changedFiles = re.findall(changeTemplate, resp)

    paths = []

    for filePath in changedFiles:
        filePath = re.split('\s+', filePath)[-2:-1][0].replace('\n', '')
        paths.append(filePath)


    print(paths)

    data = {
        'files': paths
    }

    response = json.dumps(data)

    return render(request, 'status.html', data)
    # return HttpResponse(response)



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


    data = {}

    # return render(request, 'test.html', data)
    return HttpResponse(json.dumps(data))

def handle_uploaded_file(file):
    with open('tmp/' + file.name, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    os.system('cp tmp/' + file.name + ' morda/')