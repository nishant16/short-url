# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect, get_object_or_404
from pyshorteners import Shortener
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
import random, string, json
from .models import Check
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import logging
logger = logging.getLogger(__name__)


def home(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        access_token = settings.ACCESS_TOKEN_BITLY
        http_url = request.POST['long-url']
        shortener = Shortener('Bitly', bitly_token=access_token)
        #print "My short url is {}".format(shortener.short(http_url))
        try:
            short_url = shortener.short(http_url)
        except Exception as e:
            msg = e
            return render(request, 'home.html', {'msg': msg})

        return render(request, 'short_url.html', {'short_url': short_url})
    return render(request, 'home.html')


def index_page(request):
    return render(request, 'index.html')


def redirect_original(request, slug):
    try:
        url = get_object_or_404(Check, short_id=slug) # get object, if not found return 404 error
        return redirect(url.http_url)
    except Exception as e:
        raise Http404("url does not exist")

# @csrf_exempt
# def shorten_url(request):
#     url = request.POST.get("url", '')
#     if not (url == ''):
#         short_id = get_short_code()
#         check = Check(http_url=url, short_id=short_id)
#         check.save()
#         response_data = {}
#         response_data['url'] = settings.SITE_URL + "/" + short_id
#         return HttpResponse(json.dumps(response_data), content_type="application/json")
#     return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")


def get_short_code():
    #import pdb;pdb.set_trace()
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Check.objects.get(pk=short_id)
        except:
            return short_id


@csrf_exempt
def shorten_url(request):
    url = request.POST.get("url", '')
    if not url == '' and not ' ' in url:
        try:
            check = Check.objects.get(http_url=url)
            short_id = check.short_id
        except Exception as e:
            short_id = get_short_code()
            check = Check(http_url=url, short_id=short_id)
            check.save()
            # logging.info(short_id)


        response_data = {}
        response_data['url'] = settings.SITE_URL + "/" + short_id
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")

