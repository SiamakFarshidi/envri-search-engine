from django.shortcuts import render
import glob
from os.path import isfile, join
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Index
import os
from os import walk
import json
import uuid
import numpy as np

aggregares={
    "category":{
        "terms":{
            "field": "category.keyword",
            "size": 20,
        }
    },
    "provider":{
        "terms":{
            "field": "provider.keyword",
            "size": 20,
        }
    },
    "serviceType":{
        "terms":{
            "field": "serviceType.keyword",
            "size": 20,
        }
    },
    "architecturalStyle":{
        "terms":{
            "field": "architecturalStyle.keyword",
            "size": 20,
        }
    },
    "sslSupprt":{
        "terms":{
            "field": "sslSupprt.keyword",
            "size": 20,
        }
    },
}

#-----------------------------------------------------------------------------------------------------------------------
def aggregates(request):

    return  0
#-----------------------------------------------------------------------------------------------------------------------
def genericsearch(request):
    es = Elasticsearch("http://localhost:9200")
    index = Index('webapi', es)

    try:
        term = request.GET['term']
    except:
        term = ''

    try:
        page = request.GET['page']
    except:
        page = 0

    try:
        filter = request.GET['filter']
    except:
        filter = ''

    try:
        facet = request.GET['facet']
    except:
        facet = ''


    if filter!="" and facet!="":
        request.session['filters'].append( {"term": {facet+".keyword": filter}})
    else:
        if 'filters' in request.session:
            del request.session['filters']
        request.session['filters']=[]

    page=(int(page)-1)*10

    result={}
    if term=="*" or term=="top10":
        result = es.search(
            index="webapi",
            body={
                "from" : page,
                "size" : 10,
                "query": {
                    "bool" : {
                        "must" : {
                            "match_all": {}
                        },
                        "filter": {
                            "bool" : {
                                "must" :request.session.get('filters')
                            }
                        }
                    }
                },
                "aggs":aggregares
            }
        )
    else:
        user_request = "some_param"
        query_body = {
            "from" : page, "size" : 10,
            "query": {
                "bool": {
                    "must": {
                        "multi_match" : {
                            "query": term,
                            "fields": [ "name", "description", "category", "provider", "serviceType", "architecturalStyle"],
                            "type": "best_fields",
                            "minimum_should_match": "50%"
                        }
                    },
                    "filter": {
                        "bool" : {
                            "must" :request.session.get('filters')
                        }
                    }
                }
            },
            "aggs":aggregares
        }

        result = es.search(index="webapi", body=query_body)
    lstResults=[]
    for searchResult in result['hits']['hits']:
        lstResults.append(searchResult['_source'])
    #......................
    provider=[]
    category=[]
    sslSupprt=[]
    architecturalStyle=[]
    serviceType=[]
    #......................
    for searchResult in result['aggregations']['provider']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!="Unknown" and searchResult['key']!="Data" and searchResult['key']!="Unspecified" and searchResult['key']!=""):
            pro={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            provider.append (pro)
    #......................
    for searchResult in result['aggregations']['category']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!="Unknown" and searchResult['key']!="Data" and searchResult['key']!="Unspecified" and searchResult['key']!=""):
            cat={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            category.append (cat)
    #......................
    for searchResult in result['aggregations']['sslSupprt']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!="Unknown" and searchResult['key']!="Data" and searchResult['key']!="Unspecified" and searchResult['key']!=""):
            ssl={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            sslSupprt.append (ssl)
    #......................
    for searchResult in result['aggregations']['architecturalStyle']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!="Unknown" and searchResult['key']!="Data" and searchResult['key']!="Unspecified" and searchResult['key']!=""):
            arch={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            architecturalStyle.append (arch)
    #......................
    for searchResult in result['aggregations']['serviceType']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!="Unknown" and searchResult['key']!="Data" and searchResult['key']!="Unspecified" and searchResult['key']!=""):
            service={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            serviceType.append (service)
    #......................
    facets={
        'provider':provider,
        'category':category,
        'sslSupprt':sslSupprt,
        'architecturalStyle':architecturalStyle,
        'serviceType':serviceType
    }

    numHits=result['hits']['total']['value']

    upperBoundPage=round(np.ceil(numHits/10)+1)
    if(upperBoundPage>10):
        upperBoundPage=11

    return render(request,'webapi_results.html',
                  {
                      "facets":facets,
                      "results":lstResults,
                      "NumberOfHits": numHits,
                      "page_range": range(1,upperBoundPage),
                      "cur_page": (page/10+1),
                      "searchTerm":term
                  }
                  )

#-----------------------------------------------------------------------------------------------------------------------
# Create your views here.
def indexingpipeline(request):
    es = Elasticsearch("http://localhost:9200")
    index = Index('webapi', es)

    if not es.indices.exists(index='webapi'):
        index.settings(
            index={'mapping': {'ignore_malformed': True}}
        )
        index.create()
    else:
        es.indices.close(index='webapi')
        put = es.indices.put_settings(
            index='webapi',
            body={
                "index": {
                    "mapping": {
                        "ignore_malformed": True
                    }
                }
            })
        es.indices.open(index='webapi')

    root=(os. getcwd()+"/webAPI/DB/")
    for path, subdirs, files in os.walk(root):
        for name in files:
            indexfile= os.path.join(path, name)
            indexfile = open_file(indexfile)
            newRecord={
                "name":indexfile["API name"],
                "description":indexfile["Description"],
                "url":indexfile["Url"],
                "category":indexfile["Category"],
                "provider":indexfile["Provider"],
                "serviceType":indexfile["ServiceType"],
                "documentation":indexfile["Documentation"],
                "architecturalStyle": indexfile["Architectural Style"],
                "endpointUrl":indexfile["Endpoint Url"],
                "sslSupprt":indexfile["Support SSL"],
                "logo":indexfile["Logo"]
            }

            res = es.index(index="webapi", id= uuid.uuid4(), body=newRecord)
            es.indices.refresh(index="webapi")

    return render(request,'webcontent_results.html',{})

#-----------------------------------------------------------------------------------------------------------------------
def open_file(file):
    read_path = file
    with open(read_path, "r", errors='ignore') as read_file:
        print(read_path)
        data = json.load(read_file)
        return data
#-----------------------------------------------------------------------------------------------------------------------
