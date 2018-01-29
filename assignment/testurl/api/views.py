from rest_framework.views import APIView
from rest_framework.response import Response
from hashids import Hashids
from testurl.models import Check
from .serializers import CheckSerializer
from django.conf import settings


class ShortUrl(APIView):

    def post(self, request):
        url = request.data.get('url', '')
        if not url == '' and not' ' in url:
            if 'http' not in url:
                url = 'http://' + url
                obj, created = Check.objects.get_or_create(http_url=url)
            else:
                obj, created = Check.objects.get_or_create(http_url=url)
            if created:
                hashids = Hashids(min_length=6)
                hashid = hashids.encode(obj.id)
                obj.short_id = hashid
                obj.save()
            serializer = CheckSerializer(obj)
            value = serializer.data
            value['url'] = settings.SITE_URL + '/'+serializer.data['short_id']
            return Response(value)
        return Response({'error': 'error occured'})