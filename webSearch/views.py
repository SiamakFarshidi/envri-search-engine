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
import dateutil.parser
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



def uploadFromJsonStream(request):
    libpath="/home/siamak/Downloads/res (1).json"
    #libpath="/home/siamak/Downloads/res9.json"
    title_txt=[]
    organization_ss=[]
    created_ss=[]
    content_type_ss=[]
    file_modified_dt=[]
    author_ss=[]
    producer_ss=[]
    language_s=[]
    filename_extension_s=[]
    person_ss=[]
    location_ss=[]
    id=[]
    dc_format_ss=[]
    dc_title_ss=[]
    File_Size_ss=[]
    _text_=[]
    cnt=1
    with open(libpath,"rb") as input_file:
        parser=ijson.parse(input_file)
        for doc in parser:
            if doc[2]=="_version_":
                cnt=cnt+1
                print ("Record "+str(cnt)+ " added!")
                doc={
                    "title_txt":title_txt,
                    "organization_ss": organization_ss,
                    "created_ss": created_ss,
                    "content_type_ss":content_type_ss,
                    "file_modified_dt":file_modified_dt,
                    "author_ss":author_ss,
                    "producer_ss":producer_ss,
                    "language_s":language_s,
                    "filename_extension_s":filename_extension_s,
                    "person_ss":person_ss,
                    "location_ss":location_ss,
                    "id":id,
                    "dc_format_ss":dc_format_ss,
                    "File_Size_ss":File_Size_ss,
                    "_text_":_text_
                }
                saveRecord(doc)

                title_txt.clear()
                organization_ss.clear()
                created_ss.clear()
                content_type_ss.clear()
                file_modified_dt.clear()
                author_ss.clear()
                producer_ss.clear()
                language_s.clear()
                filename_extension_s.clear()
                person_ss.clear()
                location_ss.clear()
                id.clear()
                dc_format_ss.clear()
                dc_title_ss.clear()
                File_Size_ss.clear()
                _text_.clear()
            else:
                print(doc)
                if(doc[1]=="string"):
                    if "response.docs.item.title_txt" in doc[0]:
                        title_txt.append(doc[2])
                    elif "response.docs.item.organization_ss" in doc[0]:
                        organization_ss.append(doc[2])
                    elif "response.docs.item.created_ss" in doc[0]:
                        created_ss.append(doc[2])
                    elif "response.docs.item.content_type_ss" in doc[0]:
                        content_type_ss.append(doc[2])
                    elif "response.docs.item.file_modified_dt" in doc[0]:
                        file_modified_dt.append(doc[2])
                    elif "response.docs.item.author_ss" in doc[0]:
                        author_ss.append(doc[2])
                    elif "response.docs.item.producer_ss" in doc[0]:
                        producer_ss.append(doc[2])
                    elif "response.docs.item.id" in doc[0]:
                        id.append(doc[2])
                    elif "response.docs.item.language_s" in doc[0]:
                        language_s.append(doc[2])
                    elif "response.docs.item.filename_extension_s" in doc[0]:
                        filename_extension_s.append(doc[2])
                    elif "response.docs.item.person_ss" in doc[0]:
                        person_ss.append(doc[2])
                    elif "response.docs.item.location_ss" in doc[0]:
                        location_ss.append(doc[2])
                    elif "response.docs.item.dc_format_ss" in doc[0]:
                        dc_format_ss.append(doc[2])
                    elif "response.docs.item.dc_title_ss" in doc[0]:
                        dc_title_ss.append(doc[2])
                    elif "response.docs.item.File_Size_ss" in doc[0]:
                        File_Size_ss.append(doc[2])
                    elif "response.docs.item._text_" in doc[0]:
                        _text_.append(doc[2])

#-----------------------------------------------------------------------------------------------------------------------
# Create your views here.
def saveRecord(doc):
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

    title_txt=[]
    organization_ss=[]
    created_ss=[]
    content_type_ss=[]
    file_modified_dt=[]
    author_ss=[]
    producer_ss=[]
    language_s=[]
    filename_extension_s=[]
    person_ss=[]
    location_ss=[]
    id=[]
    dc_format_ss=[]
    dc_title_ss=[]
    File_Size_ss=[]
    _text_=[]

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
        created_ss.clear()
        for txt in doc["created_ss"]:
            txt=textCleansing(txt)
            if txt and txt not in created_ss:
                created_ss.append(dateutil.parser.parse(txt))
    else:
        created_ss=["N/A"]
    #........................................................
    if "content_type_ss" in doc:
        content_type_ss.clear()
        for txt in doc["content_type_ss"]:
            txt=textCleansing(txt)
            if txt and txt not in content_type_ss:
                content_type_ss.append(txt)
    else:
        content_type_ss=["N/A"]
    #........................................................
    if "file_modified_dt" in doc:
        file_modified_dt.clear()
        for txt in doc["file_modified_dt"]:
            txt=textCleansing(txt)
            if txt and txt not in file_modified_dt:
                file_modified_dt.append(dateutil.parser.parse(txt))
    else:
        file_modified_dt=["N/A"]
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
        id.clear()
        for txt in doc["id"]:
            if txt and txt not in id:
                id.append(txt)
    else:
        id=["N/A"]
        return 0
    #........................................................
    if "dc_format_ss" in doc:
        dc_format_ss.clear()
        for txt in doc["dc_format_ss"]:
            txt=textCleansing(txt)
            if txt and txt not in dc_format_ss:
                dc_format_ss.append(txt)
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
        File_Size_ss.clear()
        for txt in doc["File_Size_ss"]:
            txt=textCleansing(txt)
            if txt and txt not in File_Size_ss:
                File_Size_ss.append(txt)
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
    bagOfWords= title_txt+organization_ss+producer_ss+_text_
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
        "text":_text_,
        "ResearchInfrastructure":getResearchInfrastructure(bagOfWords)
    }
    res = es.index(index="webcontents", id= id, body=webFeatures)
    es.indices.refresh(index="webcontents")
#----------------------------------------------------------------------------------------------------------------------- envri-search-engine
def getResearchInfrastructure(bagOfWords):
    ResearchInfrastructure=[]
    RI_list={"ICOS", "LifeWatch", "AnaEE", "AQUACOSM", "ARISE", "DANUBIUS-RI",
             "DiSSCo", "EISCAT_3D", "eLTER RI", "EMBRC", "EMSO", "EMPHASIS",
             "EPOS", "EUFAR", "Euro-Argo ERIC", "EUROFLEETS+", "EuroGOOS", "EUROCHAMP",
             "HEMERA", "IAGOS", "INTERACT", "IS-ENES", "JERICO-RI", "SeaDataNet", "SIOS" }
    for BoW in bagOfWords:
        for RI in RI_list:
            if RI.lower() in BoW.lower() and RI not in ResearchInfrastructure:
                ResearchInfrastructure.append(RI)
    return ResearchInfrastructure
#----------------------------------------------------------------------------------------------------------------------- envri-search-engine
def textCleansing(txt):
    if type(txt)==str:
        res = isinstance(txt, str)
        if res:
            txt=re.sub(r'[^A-Za-z0-9 .-\?/:,;~%$#*@!&+=]+', '', txt)
    if len(txt)==1:
        txt=""
    return txt
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
    return render(request,'webcontent_results.html',{"results":lstResults, "NumberOfHits": result['hits']['total']['value']})

