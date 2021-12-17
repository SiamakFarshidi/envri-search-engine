from django.conf.urls import url,include
from InferenceEngine import views,models
from opensemanticsearch import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^index', views.index, name='index'),
	url(r'^REST-API', views.processSingleReq, name='processSingleReq'),
    url(r'^home', views.home, name='home'),
    url(r'^addNew', views.addNew, name='addNew'),
    url(r'^count', views.count, name='count')
    #url(r'^overview', views.overview, name='overview')
    #url(r'^detail', views.detail, name='detail')
]
