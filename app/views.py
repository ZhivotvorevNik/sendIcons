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


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
MORDA_PATH = SITE_ROOT + '/../morda/'

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

    settings = []

    # Получаем флаги (должны быть вида settings_[имя])
    for param in params:
        result = re.compile('settings_(.*)').match(param)
        if result:
            settings.append(result.group(1))

    if 'icon' in files:
        uploadFile = files['icon']
        serviceName = params['service']

        extMap = {
            'image/svg+xml': 'svg',
            'image/png': 'png'
        }

        if uploadFile.content_type in extMap:
            fileExtention = extMap[uploadFile.content_type]
            filePath = handle_uploaded_file(uploadFile, serviceName, fileExtention)

            optimizeImg(filePath, fileExtention)
            moveToDest(filePath, fileExtention, serviceName,  settings)

            data = {
                'status': 'ok',
                'imgSrc': filePath
            }

        else:
            data = {
                'status': 'error'
            }


    response = json.dumps(data)

    return HttpResponse(response)


def status(request):
    os.chdir(MORDA_PATH)
    resp, err = Popen('git status', shell=True, stdout=PIPE).communicate()
    resp = str(resp, 'utf8')

    os.chdir(SITE_ROOT)


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
    os.chdir(MORDA_PATH)
    os.system('git add -A')
    os.system('git checkout -f')

    os.chdir(SITE_ROOT)

    data = {
        'status': 'ok'
    }

    return HttpResponse(json.dumps(data))

def commit(request):
    params = request.POST
    files = []

    message = 'HOME-0: Добавлены иконки в /all'

    for key, val in params.items():
        if key == 'commit__message' and val:
            message = val
        if val == 'on':
            files.append(key)

    if len(files):
        files.insert(0, 'git add')
        add_command = ' '.join(files)

        os.chdir(MORDA_PATH)

        os.system('git stash')
        os.system('git pull origin dev')
        os.system('git stash pop')
        os.system(add_command)
        os.system('git commit -m "' + message + '"')

        os.chdir(SITE_ROOT)

        data = {
            'status': 'ok',
            'message': message
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
    cookies = request.COOKIES
    meta = request.META
    useragent = request.META.get('HTTP_USER_AGENT')
    result = user_agents.parse(useragent)
    isTouch = result.is_touch_capable

    files = os.listdir(SITE_ROOT + '/../tmp/')

    print(files)

    services = Service.objects.order_by('name')


    data = files

    # return render(request, 'test.html', data)
    return HttpResponse(json.dumps(data))


# Добавить сжатие, нормальные имена, перенос в правильные места
def handle_uploaded_file(file, serviceName, fileExtention):
    path = SITE_ROOT + '/../tmp/' + serviceName + '.' + fileExtention
    with open(path, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    return path

# TODO добавить оптимизацию
def optimizeImg(path, ext):
    if ext == 'png':
        optimizePng(path)
    elif ext == 'svg':
        optimizeSvg(path)
    else:
        print('Другое расширение')
        return

def optimizeSvg(path):
    print('оптимизация svg...')
    return


def optimizePng(path):
    print('оптимизация png...')
    return


def moveToDest(path, fileExtention, serviceName, settings):
    isTr = 'turkey' in settings
    files = []
    for setting in settings:
        if setting == 'turkey':
            pass
        else:
            destPath = getDestPath(serviceName, setting, fileExtention, isTr)
            os.system('cp ' + path + ' ' + MORDA_PATH + destPath)

def getDestPath(serviceName, setting, extention, isTr):
    prefix = '_tr' if isTr else ''

    if (setting == 'big'):
        return 'tmpl/everything/blocks/common-all/services-main/services-main.inline/' + serviceName + prefix + '.' + extention
    elif (setting == 'small'):
        return 'tmpl/everything/blocks/common-all/services-all/services-all.inline/' + serviceName + '_small' + prefix + '.' + extention
    elif (setting == '404'):
        return 'tmpl/white/blocks/404/services/services.inline/service-' + serviceName + prefix + '.' + extention

def minifyPng(path):
    ext - 5