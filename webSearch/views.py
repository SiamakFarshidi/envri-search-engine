from django.shortcuts import render
from django.forms.widgets import NullBooleanSelect, Widget
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import simplejson
from urllib.request import urlopen
import urllib
from datetime import datetime
from elasticsearch import Elasticsearch
from glob import glob
from elasticsearch_dsl import Search, Q, Index
from elasticsearch_dsl.query import MatchAll
from django.core import serializers
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Index
import re
import ijson
aggregares={
    "locations":{
        "terms":{
            "field": "locations.keyword",
            "size": 20,
        }
    },
    "person":{
        "terms":{
            "field": "person.keyword",
            "size": 20,
        }
    },
    "organizations":{
        "terms":{
            "field": "organizations.keyword",
            "size": 20,
        }
    },
    "authors":{
        "terms":{
            "field": "authors.keyword",
            "size": 20,
        }
    },
    "producers":{
        "terms":{
            "field": "producers.keyword",
            "size": 20,
        }
    },
}

# Create your views here.
def uploadFromJsonLibrary(request):

    es = Elasticsearch("http://localhost:9200")
    index = Index('webcontents', es)

    if not es.indices.exists(index='webcontents'):
        index.settings(
            index={'mapping': {'ignore_malformed': True}}
        )
        index.create()
    else:
        es.indices.close(index='webcontents')
        put = es.indices.put_settings(
            index='webcontents',
            body={
                "index": {
                    "mapping": {
                        "ignore_malformed": True
                    }
                }
            })
        es.indices.open(index='webcontents')


    #libpath="/home/siamak/Downloads/res (1).json"
    libpath="/home/siamak/Downloads/res11.json"
    webcontents = open(libpath,"r")
    webcontents_json = json.loads(webcontents.read())

    _text_=[]
    dc_title_ss=[]
    location_ss=[]
    person_ss=[]
    filename_extension_s=[]
    language_s=[]
    producer_ss=[]
    author_ss=[]
    organization_ss=[]
    title_txt=[]
    for doc in webcontents_json["response"]["docs"]:
        #........................................................
        if "title_txt" in doc:
            title_txt.clear()
            for txt in doc["title_txt"]:
                txt=textCleansing(txt)
                if txt and txt not in title_txt:
                    title_txt.append(txt)
        else:
            title_txt=["N/A"]
        #........................................................
        if "organization_ss" in doc:
            organization_ss.clear()
            for txt in doc["organization_ss"]:
                txt=textCleansing(txt)
                if txt and txt not in organization_ss:
                    organization_ss.append(txt)
        else:
            organization_ss=["N/A"]
        #........................................................
        if "created_ss" in doc:
            created_ss=(doc["created_ss"])
        else:
            created_ss="N/A"
        #........................................................
        if "content_type_ss" in doc:
            content_type_ss=(doc["content_type_ss"])
        else:
            content_type_ss="N/A"
        #........................................................
        if "file_modified_dt" in doc:
            file_modified_dt=(doc["file_modified_dt"])
        else:
            file_modified_dt="N/A"
        #........................................................
        if "author_ss" in doc:
            author_ss.clear()
            for txt in doc["author_ss"]:
                txt=textCleansing(txt)
                if txt and txt not in author_ss:
                    author_ss.append(txt)
        else:
            author_ss=["N/A"]
        #........................................................
        if "producer_ss" in doc:
            producer_ss.clear()
            for txt in doc["producer_ss"]:
                txt=textCleansing(txt)
                if txt and txt not in producer_ss:
                    producer_ss.append(txt)
        else:
            producer_ss=["N/A"]
        #........................................................
        if "language_s" in doc:
            language_s.clear()
            for txt in doc["language_s"]:
                txt=textCleansing(txt)
                if txt and txt not in language_s:
                    language_s.append(txt)
        else:
            language_s=["N/A"]
        #........................................................
        if "filename_extension_s" in doc:
            filename_extension_s.clear()
            for txt in doc["filename_extension_s"]:
                txt=textCleansing(txt)
                if txt and txt not in filename_extension_s:
                    filename_extension_s.append(txt)
        else:
            filename_extension_s=["N/A"]
        #........................................................
        if "person_ss" in doc:
            person_ss.clear()
            for txt in doc["person_ss"]:
                txt=textCleansing(txt)
                if txt and txt not in person_ss:
                    person_ss.append(txt)
        else:
            person_ss=["N/A"]
        #........................................................
        if "location_ss" in doc:
            location_ss.clear()
            for txt in doc["location_ss"]:
                txt=textCleansing(txt)
                if txt and txt not in location_ss:
                    location_ss.append(txt)
        else:
            location_ss=["N/A"]
        #........................................................
        if "id" in doc:
            id=(doc["id"])
        else:
            id=["N/A"]
            continue
        #........................................................
        if "dc_format_ss" in doc:
            dc_format_ss=(doc["dc_format_ss"])
        else:
            dc_format_ss=["N/A"]
        #........................................................
        if "dc_title_ss" in doc:
            dc_title_ss.clear()
            for txt in doc["dc_title_ss"]:
                txt=textCleansing(txt)
                if txt and txt not in dc_title_ss:
                    dc_title_ss.append(txt)
        else:
            dc_title_ss=["N/A"]
        #........................................................
        if "File_Size_ss" in doc:
            File_Size_ss=(doc["File_Size_ss"])
        else:
            File_Size_ss=["N/A"]
        #........................................................
        if "_text_" in doc:
            _text_.clear()
            for txt in doc["_text_"]:
                txt=textCleansing(txt)
                if txt and txt not in _text_:
                    _text_.append(txt)
        else:
            _text_=["N/A"]
        #........................................................

        webFeatures={
            "title":title_txt,
            "organizations": organization_ss,
            "creation_date": created_ss,
            "content_type":content_type_ss,
            "modification_date":file_modified_dt,
            "authors":author_ss,
            "producers":producer_ss,
            "language":language_s,
            "file_extensions":filename_extension_s,
            "person":person_ss,
            "locations":location_ss,
            "id":id,
            "file_formats":dc_format_ss,
            "file_size":File_Size_ss,
            "text":_text_
        }
        res = es.index(index="webcontents", id= id, body=webFeatures)
        es.indices.refresh(index="webcontents")

    response_data = {}
    response_data['result'] = ""
    response_data['message'] = 'The indexing process of the  dataset repository has been initiated!'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

#----------------------------------------------------------------------------------------------------------------------- envri-search-engine
def textCleansing(txt):
    result=""
    res = isinstance(txt, str)
    if res:
        result=re.sub(r'[^A-Za-z0-9 .]+', '', txt)

    return result
#----------------------------------------------------------------------------------------------------------------------- envri-search-engine
def aggregates(request):
    print("indexing...")


    response_data = {}
    response_data['result'] = ""
    response_data['message'] = 'The indexing process of the dataset repository has been initiated!'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

#-----------------------------------------------------------------------------------------------------------------------
def genericsearch(request):
    es = Elasticsearch("http://localhost:9200")
    index = Index('webcontents', es)

    try:
        term = request.GET['term']
    except:
        term = ''

    try:
        page = request.GET['page']
    except:
        page = 0

    page=page*10
    print(term)
    result={}
    if term=="*":
        result = es.search(
            index="webcontents",
            body={
                "from" : 0, "size" : 1000,
                "query": {
                    "match_all": {}
                },
                "aggs":aggregares
            }
        )
    else:
        user_request = "some_param"
        query_body = {
            "from" : 0, "size" : 1000,
            "query": {
                "multi_match" : {
                    "query": term,
                    "fields": [ "organizations", "title", "publisher", "authors", "producers", "file_extensions", "text"]
                }
            },
            "aggs":aggregares
        }
        result = es.search(index="webcontents", body=query_body)
        lstResults=[]
        for searchResult in result['hits']['hits']:
            lstResults.append(searchResult['_source'])

    #envri-statics
    print("Got %d Hits:" % result['hits']['total']['value'])
    #return JsonResponse(result, safe=True, json_dumps_params={'ensure_ascii': False})
    return render(request,'ContentResult.html',{"results":lstResults, "NumberOfHits": result['hits']['total']['value']})

