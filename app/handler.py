from django.shortcuts import render_to_response
from django.http import HttpResponse
import user_agents
import json


def save (request):
    params = request.POST
    cookies = request.COOKIES
    meta = request.META
    useragent = request.META.get('HTTP_USER_AGENT')
    result = user_agents.parse(useragent)
    isTouch = result.is_touch_capable

    res = json.dumps(params)

    print(result.browser)
    data = {
        'params': params,
        'COOKIES': cookies,
        'META': meta,
        'useragent': result
    }
    # return render_to_response('test.html', data)
    return HttpResponse(res)