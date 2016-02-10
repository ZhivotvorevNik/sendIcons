from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import time
import user_agents

def index(request):

    params = request.GET
    meta = request.META
    st = 'HELLO, '
    date = time.strftime('%H:%M, %d %B %Y' ,time.localtime(time.time()))
    data = {
        'MESSAGE': st,
        'USER': 'nizhi',
        'ONLINE': False,
        'dates': ['123', '324324', '324324', '32432432', '565465', '546546'],
        'PARAMS': params,
        'DATE': date,
        'req': params,
        'metas': meta
    }
    return render_to_response('index.html', data, context_instance=RequestContext(request))

def test(request):
    params = request.POST
    cookies = request.COOKIES
    meta = request.META
    useragent = request.META.get('HTTP_USER_AGENT')
    result = user_agents.parse(useragent)
    isTouch = result.is_touch_capable

    print(result.browser)
    data = {
        'params': params,
        'COOKIES': cookies,
        'META': meta,
        'useragent': result
    }
    return render_to_response('test.html', data)
    # return HttpResponse("Do something")