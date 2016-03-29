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
    cookies = request.COOKIES
    meta = request.META
    useragent = request.META.get('HTTP_USER_AGENT')
    result = user_agents.parse(useragent)
    isTouch = result.is_touch_capable


    data = {
        'services': services
    }

    return render(request, 'index.html', data, context_instance=RequestContext(request))

def add(request):
    params = request.POST
    files = request.FILES
    data = {'status': 'error'}

    if 'icon' in files:
        uploadFile = files['icon']
        allowTypes = ['image/png', 'image/svg+xml']
        serviceName = params['service']

        if uploadFile.content_type in allowTypes:
            handle_uploaded_file(uploadFile, serviceName)
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

    data = {
        'files': paths
    }

    return render(request, 'status.html', data)


def checkout(request):
    os.chdir('morda')
    os.system('git add -A')
    os.system('git checkout -f')

    os.chdir('../')

    data = {
        'status': 'ok'
    }

    return HttpResponse(json.dumps(data))

def commit(request):
    params = request.POST
    files = []

    for key, val in params.items():
        if val == 'on':
            files.append(key)

    if len(files):
        files.insert(0, 'git add')
        add_command = ' '.join(files)

        os.chdir('morda')

        os.system('git stash')
        os.system('git pull origin dev')
        os.system('git stash pop')
        os.system(add_command)
        os.system('git commit -m "HOME-0: Добавлены иконки"')

        os.chdir('../')

        data = {
            'status': 'ok',
            'params': params
        }
    else:
        data = {
            'status': 'error',
            'error': 'nodata'
        }

    return HttpResponse(json.dumps(data))


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
    files = request.FILESnancat
    cookies = request.COOKIES
    meta = request.META
    useragent = request.META.get('HTTP_USER_AGENT')
    result = user_agents.parse(useragent)
    isTouch = result.is_touch_capable

    services = Service.objects.order_by('name')


    data = {}

    # return render(request, 'test.html', data)
    return HttpResponse(json.dumps(data))


# Добавить сжатие, нормальные имена, перенос в правильные места
def handle_uploaded_file(file, serviceName):
    extMap = {
        'image/svg+xml': 'svg',
        'image/png': 'png'
    }


    path = 'tmp/' + serviceName + '.' + extMap[file.content_type]
    with open(path, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    os.system('cp ' + path + ' morda/')

def minifyPng(path):
    ext - 5