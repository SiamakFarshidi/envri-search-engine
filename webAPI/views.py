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
    page=(int(page)-1)*10

    result={}
    if term=="*" or term=="top10":
        result = es.search(
            index="webapi",
            body={
                "from" : page, "size" : 10,
                "query": {
                    "match_all": {}
                },
                "aggs":aggregares
            }
        )
    else:
        user_request = "some_param"
        query_body = {
            "from" : page, "size" : 10,
            "query": {
                "multi_match" : {
                    "query": term,
                    "fields": [ "name", "description", "category", "provider", "serviceType", "architecturalStyle"]
                }
            },
            "aggs":aggregares
        }
        result = es.search(index="webapi", body=query_body)
    lstResults=[]
    for searchResult in result['hits']['hits']:
        lstResults.append(searchResult['_source'])

    #print("Got %d Hits:" % result['hits']['total']['value'])
    #return JsonResponse(result, safe=True, json_dumps_params={'ensure_ascii': False})


    numHits=result['hits']['total']['value']

    upperBoundPage=round(np.ceil(numHits/10)+1)
    if(upperBoundPage>10):
        upperBoundPage=11

    return render(request,'webapi_results.html',
                  {
                      "results":lstResults,
                      "NumberOfHits": numHits,
                      "page_range": range(1,upperBoundPage),
                      "cur_page": (page/10+1)
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
