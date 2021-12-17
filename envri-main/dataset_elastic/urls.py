from django.conf.urls import url,include
from dataset_elastic import views,models
from django.conf.urls.static import static


urlpatterns = [
	#url(r'^index', views.index, name='index'),
    url(r'^home', views.home, name='home'),
    url(r'^result', views.home, name='result'),
    url(r'^search', views.search_index, name='search_index'),
    url(r'^rest', views.rest, name='rest')
]
