from django.conf.urls import url,include
from webSearch import views,models
from django.conf.urls.static import static


urlpatterns = [
	#url(r'^index', views.index, name='index'),
    url(r'^uploadFromJsonLibrary', views.uploadFromJsonLibrary, name='uploadFromJsonLibrary'),
    url(r'^genericsearch', views.genericsearch, name='genericsearch'),
    url(r'^aggregates', views.aggregates, name='aggregates')
]
