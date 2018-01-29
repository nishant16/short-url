# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect, get_object_or_404
from pyshorteners import Shortener
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404,JsonResponse
import random, string, json
from .models import Check
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import logging
logger = logging.getLogger(__name__)
from hashids import Hashids
from django.core import serializers


# def short_url_way(request):
#     #import pdb;pdb.set_trace()
#     url = request.POST.get('url', '')
#     if not url == '' and not ' ' in url:
#         try:
#             obj = Check.objects.get(http_url=url)
#             hashid = obj.short_id
#         except Exception as e:
#             obj = Check.objects.create(http_url=url)
#             hashids = Hashids(min_length=4)
#             hashid = hashids.encode(obj.id)
#             obj.short_id = hashid
#             obj.save()
#         url_link = {'link': settings.SITE_URL + '/r/' + hashid, 'id':obj.id}
#         return HttpResponse(json.dumps(url_link), content_type="application/json")
#     return HttpResponse(json.dumps({'error':"error occured"}), content_type="application/json")


def page(request):
    return render(request, 'page.html')


def short_url_way(request):
    url = request.POST.get('url', '')
    if not url == '' and not ' ' in url:
        if 'http' not in url:
            url= 'http://' + url
            obj, created = Check.objects.get_or_create(http_url=url)
        else:
            obj, created = Check.objects.get_or_create(http_url=url)
        hashid = obj.short_id
        new_hash = 0
        if created:
            new_hash = 1
            hashids = Hashids(min_length=7)
            hashid = hashids.encode(obj.id)
            obj.short_id = hashid
            obj.save()
        url_link = {'status_code': 200, 'link': settings.SITE_URL + '/' + hashid, 'long_url': url, "hash": hashid, "new_hash":new_hash }
        return HttpResponse(json.dumps(url_link), content_type="application/json")
    return HttpResponse(json.dumps({'status_code': 500, 'status_txt': "INVALID_ARG_URL"}), content_type="application/json")


def redirect_original(request, slug):
    try:
        url = get_object_or_404(Check, short_id=slug)
        return redirect(url.http_url)
    except Exception as msg:
        raise msg


def url_method():
    import csv
    csvopenfile = open('/home/nishantagarwal/hdfc_falsification_sheet.csv', 'rb')
    reader = csv.reader(csvopenfile)
    file_url = [row[0] for row in reader]
    csvwritefile = open('/home/nishantagarwal/hdfc_falsification_sheet.csv', 'wb')
    writefile = csv.writer(csvwritefile)
    # import pdb;pdb.set_trace()
    check_params = Check.objects.filter(http_url__in=file_url).values("http_url", 'short_id')
    for url in check_params:
        url_link = settings.SITE_URL + '/' + url['short_id']
        writefile.writerow([url['http_url'], url_link])
    exist_url = Check.objects.filter(http_url__in=file_url).values_list("http_url", flat=True)
    new_url_list = list(set(file_url) - set(exist_url))
    try:
        last_id = Check.objects.all().last().id + 1
    except AttributeError:
        last_id = 1

    check_objs = []
    for url in new_url_list:
        if 'http://' not in url:
            http_url = 'http://' + url
        hashids = Hashids(min_length=6)
        hashid = hashids.encode(last_id)
        last_id += 1
        url_link = settings.SITE_URL + '/' + hashid
        writefile.writerow([url, url_link])
        check_objs.append(Check(http_url=http_url, short_id=hashid))
    Check.objects.bulk_create(check_objs)


def csv_method():
    import csv
    csvopenfile = open('/home/nishantagarwal/hdfc_falsification_sheet.csv', 'rb')
    reader = csv.reader(csvopenfile)
    # long_url = []
    # for row in reader:
    #     long_url.append(row[0])
    long_url = [row[0] for row in reader]
    csvwritefile = open('/home/nishantagarwal/hdfc_falsification_sheet.csv', 'wb')
    writefile = csv.writer(csvwritefile)
    check_params = Check.objects.filter(http_url__in=long_url).values("http_url", 'short_id')

    for url in check_params:
        url_link = settings.SITE_URL + '/' + url['short_id']

        writefile.writerow([url['http_url'], url_link])

    http_url_list = []
    for url in long_url:
        if not url == '' and not ' ' in url:
            if 'http' not in url:
                url = 'http://' + url
            http_url_list.append(url)

    exist_url = Check.objects.filter(http_url__in=http_url_list).values_list("http_url", flat=True)
    new_url_list = list(set(long_url)-set(exist_url))

    last_id = Check.objects.all().last().id + 1
    check_objs = []
    for http_url in new_url_list:
        hashids = Hashids(min_length=6)
        hashid = hashids.encode(last_id)
        last_id += 1
        url_link = settings.SITE_URL + '/' + hashid
        writefile.writerow([http_url, url_link])
        check_objs.append(Check(http_url=http_url, short_id=hashid))
    Check.objects.bulk_create(*check_objs)
    csvopenfile.close()
    csvwritefile.close()

    for url in long_url:
        if not url == '' and not ' ' in url:
            if 'http' not in url:
                http_url = 'http://' + url
                obj, created = Check.objects.get_or_create(http_url=http_url)
            else:
                obj, created = Check.objects.get_or_create(http_url=url)
            hashid = obj.short_id
            if created:
                hashids = Hashids(min_length=6)
                hashid = hashids.encode(obj.id)
                obj.short_id = hashid
                obj.save()
            url_link = settings.SITE_URL + '/' + hashid

            writefile.writerow([url, url_link])
    csvopenfile.close()
    csvwritefile.close()


def home(request):
    if request.method == 'POST':
        access_token = settings.ACCESS_TOKEN_BITLY
        http_url = request.POST['long-url']
        shortener = Shortener('Bitly', bitly_token=access_token)
        try:
            short_url = shortener.short(http_url)
        except Exception as e:
            msg = e
            return render(request, 'home.html', {'msg': msg})

        return render(request, 'short_url.html', {'short_url': short_url})
    return render(request, 'home.html')


def index_page(request):
    return render(request, 'index.html')



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


def check_get(request):
    url = request.GET.get('url', '')
    data = serializers.serialize("xml", Check.objects.all()) ##it will serialize the data in to xml

    if not url == '' and not ' ' in url:
        try:
            obj = Check.objects.get(http_url=url)
            hashid = obj.short_id
        except Exception as e:
            obj = Check.objects.create(http_url=url)
            hashids = Hashids(min_length=4)
            hashid = hashids.encode(obj.id)
            obj.short_id = hashid
            obj.save()

        url_link = {'link': settings.SITE_URL + '/r/' + hashid, 'id':obj.id}
        # return HttpResponse(json.dumps(url_link), content_type="application/json")
        return JsonResponse(url_link)
        # return HttpResponse(url_link) ##it will not work as json is not dumped
        # return JsonResponse([1,2,3], safe=False) ##set safe false for data type except dict
    return HttpResponse(json.dumps({'error': "error occured"}), content_type="application/json")


def data_get(request):
    return render(request, 'data_get.html')

