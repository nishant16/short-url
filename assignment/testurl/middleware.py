import time
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class StatMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # import pdb;
        # pdb.set_trace()
        print "request"
        request.start_time = time.time()


    def process_response(self,request,response):
        # import pdb;
        # pdb.set_trace()
        print "response"
        duration = time.time()-request.start_time
        print duration
        # response["X-Page-Generation-Duration-ms"] = int(duration * 1000)
        return response
