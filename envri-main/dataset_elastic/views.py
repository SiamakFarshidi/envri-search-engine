from django.forms.widgets import NullBooleanSelect, Widget
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
from urllib.request import urlopen
from datetime import datetime
from elasticsearch import Elasticsearch
from glob import glob
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MatchAll

es = Elasticsearch("http://localhost:9200")

def rest(request):
	try:
		term = request.GET['term']
	except:
		term = ''
	try:
		year_from = request.GET['year_from']
	except:
		year_from = "0"
	try:
		year_to = request.GET['year_to']
	except:
		year_to = "3000"
	try:
		lon = request.GET['lon']
	except:
		lon = "0"
	try:
		lat = request.GET['lat']
	except:
		lat= "0"
	try:
		station = request.GET['station']
	except:
		station = '*'
	try:
		genre = request.GET['genre']
	except:
		genre='*'
	try:
		author = request.GET['author']
	except:
		author = '*'
	try:
		distributor = request.GET['distributor']
	except:
		distributor = '*'
	try:
		keywords = request.GET['keywords']
	except:
		keywords = '*'
	try:
		abstract = request.GET['abstract']
	except:
		abstract = '*'

	print(station)

	result = esearch(all_fields = term, year_from=year_from, year_to=year_to, lon=lon, 
					lat=lat, station=station, genre=genre, author=author, distributor=distributor,
					keywords=keywords, abstract=abstract)

	return JsonResponse(result, safe = False, json_dumps_params={'ensure_ascii': False})

#-------------------------------------------------------------------------

def home(request):
    #index_elastic()
    context = {}
    #context['form'] = SelectionForm()
    #context['result'] = SelectionForm.fields
    return render(request, "home.html", context)

def result(request):
    context = {}
    #context['result'] = SelectionForm()
    return render(request, "result.html")

#-------------------------------------------------------------------------

def search_index(request):
	results = []
	keywords_term = ""
	abstract_term = ""
	all_fields_term = ""
	year_from_term = ""
	year_to_term = ""

	"""
	if request.GET.get('keywords') and request.GET.get('abstract'):
		keywords_term = request.GET['keywords']
		abstract_term = request.GET['abstract']
	elif request.GET.get('keywords'):
		keywords_term = request.GET['keywords']
	elif request.GET.get('abstract'):
		abstract_term = request.GET['abstract']
	elif request.GET.get('all_fields'):
		all_fields_term = request.GET['all_fields']
	"""

	try:
		keywords_term = request.GET['keywords']
	except:
		pass
	try:
		abstract_term = request.GET['abstract']
	except:
		pass
	try:
		all_fields_term = request.GET['all_fields']
	except:
		pass
	try:
		year_from_term = request.GET['year_from']
	except:
		pass
	try:
		year_to_term = request.GET['year_to' ]
	except:
		pass

	search_term = keywords_term or abstract_term or all_fields_term or year_from_term or year_to_term
	
	#print(search_term)
	#results = esearch(keywords = keywords_term, abstract=abstract_term, all_terms = all_fields_term)
	results = esearch(keywords = keywords_term,
					  abstract = abstract_term, 
					  all_fields = all_fields_term, 
					  year_from = year_from_term, 
					  year_to = year_to_term)

	#print(results)
	context = {'results': results, 'count': len(results), 'search_term': search_term }
	return render(request, 'search.html', context) 

#----------------------------------------------------------------

#----------------------------------------------------------------

def esearch(keywords = "",
			abstract = "",
			all_fields = "",
			year_from = "",
			year_to = "",
			lon = "",
			lat= "",
			station= "",
			genre= "",
			author="",
			distributor="",
			):

	client = es	

	if keywords == "*":
		filter_type_keywords = "wildcard"
	else:
		filter_type_keywords = "match"

	if abstract == "*":
		filter_type_abstract = "wildcard"
	else:
		filter_type_abstract = "match"

	if station == '*':
		filter_type_provider = "wildcard"
	else:
		filter_type_provider = "term"
	
	if genre == '*':
		filter_type_genre = "wildcard"
	else:
		filter_type_genre = "term"

	if author == '*':
		filter_type_author = "wildcard"
	else:
		filter_type_author = "term"

	if distributor == '*':
		filter_type_distributor = "wildcard"
	else:
		filter_type_distributor = "term"

	if lon == "0":
		lon_gte = "-90.0"
		lon_lte = "90.0"

	else:
		lon_gte = (float(lon) - 1)
		lon_lte = (float(lon) + 1)

	if lat == "0":
		lat_gte = "-90.0"
		lat_lte = "90.0"

	else:
		lat_gte = (float(lat) - 1)
		lat_lte = (float(lat) + 1)

	q = Q("bool",

		should=[
		Q("match", keywords=keywords), 
		Q("match", abstract = abstract),
		Q("match", keywords=all_fields), 
		Q("match", abstract = all_fields),
		Q("match", name = all_fields),
		Q("match", material = all_fields),
		Q("match", publisher = all_fields),
		Q("match", description = all_fields),
		Q("match", provider = all_fields),
		Q("match", distributionInfo = all_fields),
		Q("match", about = all_fields),
		Q("match", citation = all_fields),
		Q("match", responsibleParty = all_fields),
		Q("match", creator = all_fields),
		Q("match", accountablePerson = all_fields),
		Q("match", locationCreated = all_fields),
		],
		minimum_should_match=1
	)

	s = Search(using = client, index = "envri")\
			.filter("range", temporal = {'gte': year_from, 'lte': year_to})\
			.filter("range", longitude = {'gte': lon_gte, 'lte': lon_lte})\
			.filter("range", latitude = {'gte': lat_gte, 'lte': lat_lte})\
			.filter(filter_type_provider, provider = station)\
			.filter(filter_type_genre, genre = genre)\
			.filter(filter_type_distributor, distributor = distributor)\
			.filter(filter_type_author, author = author)\
			.query(q)[:10000]


			
	#.filter("range", spatialCoverage = {'gte': lon - 1, 'lte': lon + 1})\
	response = s.execute()
	print(filter_type_provider)
	#print("%d hits found." % response.hits.total)
	search = get_results_rest(response)
	return search

def get_results_rest(response):
	results = {}
	for hit in response:
		result = {
			'identifier': hit.identifier,
			'name' : hit.name,
			'temporal' : hit.temporal,
			'author' : [name for name in hit.author],
			'landing_page' : hit.landing_page,
			'keywords' : [keyword for keyword in hit.keywords],
			'distributor' : hit.distributor,
			'station': hit.provider,
			'genre' : hit.genre,
			'longitude': hit.longitude,
			'latitude': hit.latitude
		}
		results[hit.identifier] = result
	return results

def get_results(response):
	results = []
	for hit in response:
		result_tuple = (hit.identifier, hit.landing_page, hit.name)
		results.append(result_tuple)
	return results

#-------------------------------------------------------------

#-------------------------------------------------------------
