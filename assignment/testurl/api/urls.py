from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^short_url/$', views.ShortUrl.as_view(), name='short_url'),

]