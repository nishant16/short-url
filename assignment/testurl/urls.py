from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.home, name='index'),
    url(r'^index/$', views.index_page, name='index_page'),
    url(r'^shorten_url/$', views.shorten_url, name='shorten_url'),
    url(r'^page/$', views.page, name='page'),
    url(r'^short_url_way/$', views.short_url_way, name='short_url_way'),
    url(r'^data_get/$', views.data_get, name='data_get'),
    url(r'^check_get/$', views.check_get, name='check_get'),
]


urlpatterns += [
    url(r'^(?P<slug>[-\w]+)/$', views.redirect_original, name='redirect_url'),
    ]
