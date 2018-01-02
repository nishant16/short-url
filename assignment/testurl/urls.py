from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.home, name='index'), #ex:/
    url(r'^index/$', views.index_page, name='index_page'),
    url(r'^shorten_url/$',views.shorten_url,name='shorten_url'),
    url(r'^(?P<slug>[-\w]*)/$', views.redirect_original, name='redirect_url')
]