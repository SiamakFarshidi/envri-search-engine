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
import nltk
import numpy as np
nltk.download('words')
words = set(nltk.corpus.words.words())


ResearchInfrastructures={
    'icos-cp.eu': {
        'id': 1,
        'url':'https://www.icos-cp.eu/',
        'label': 'Multi-domain',
        'title': 'Integrated Carbon Observation System',
        'acronym':'ICOS'
    },
    'seadatanet.org': {
        'id': 2,
        'url':'https://www.seadatanet.org/',
        'label': 'Marine',
        'title': 'Pan-European infrastructure for ocean and marine data management',
        'acronym':'SeaDataNet'
    },
    'lifewatch.eu': {
        'id': 3,
        'url':'https://www.lifewatch.eu/',
        'label': 'Multi-domain',
        'title': 'An e-Infrastructure for basic research on biodiversity and ecosystems',
        'acronym':'LifeWatch'
    },
    'anaee.eu':{
        'id': 4,
        'url':'https://www.anaee.eu/',
        'label': 'Terrestrial ecosystem / Biodiversity',
        'title': 'Analysis and Experimentation on Ecosystems',
        'acronym':'AnaEE'
    },
    'actris.eu':{
        'id': 5,
        'url':'https://www.actris.eu/',
        'label': 'Atmospheric',
        'title': 'The Aerosol, Clouds and Trace Gases Research Infrastructure',
        'acronym':'ACTRIS'
    },
    'aquacosm.eu':{
        'id': 6,
        'url':'https://www.aquacosm.eu/',
        'label': 'Marine / Freshwater',
        'title': 'EU network of mesocosms facilities for research on marine and freshwater',
        'acronym':'AQUACOSM'
    },
    'arise-project.eu':{
        'id': 7,
        'url':'http://arise-project.eu/',
        'label': 'Atmosphere',
        'title': 'Atmospheric dynamics Research InfraStructure in Europe',
        'acronym':'ARISE'
    },
    'danubius-pp.eu':{
        'id': 8,
        'url':'https://danubius-pp.eu/',
        'label': 'River / Marine',
        'title': 'Preparatory Phase For The Paneuropean Research Infrastructure',
        'acronym':'DANUBIUS-RI'
    },
    'dissco.eu':{
        'id': 9,
        'url':'https://www.dissco.eu/',
        'label': 'Terrestrial ecosystem / Biodiversity',
        'title': 'Distributed System of Scientific Collections',
        'acronym':'DiSSCo'
    },
    'eiscat.se':{
        'id': 10,
        'url':'https://eiscat.se/',
        'label': 'Atmospheric',
        'title': 'EISCAT Scientific Association',
        'acronym':'EISCAT 3D'
    },
    'lter-europe.net':{
        'id': 11,
        'url':'https://www.lter-europe.net/',
        'label': 'Biodiversity / Ecosystems',
        'title': 'Long-Term Ecosystem Research in Europe',
        'acronym':'eLTER RI'
    },
    'embrc.eu':{
        'id': 12,
        'url':'https://www.embrc.eu/',
        'label': 'Marine / Biodiversity',
        'title': 'Long-Term Ecosystem Research in Europe',
        'acronym':'EMBRC'
    },
    'emso.eu':{
        'id': 13,
        'url':'https://emso.eu/',
        'label': 'Multi-domain',
        'title': 'European Multidisciplinary Seafloor and water column Observatory',
        'acronym':'EMSO'
    },
    'emphasis.plant-phenotyping.eu':{
        'id': 14,
        'url':'https://emphasis.plant-phenotyping.eu/',
        'label': 'Terrestrial Ecosystem',
        'title': 'European Infrastructure for Plant Phenotyping',
        'acronym':'EMPHASIS'
    },
    'epos-eu.org':{
        'id': 15,
        'url':'https://www.epos-eu.org/',
        'label': 'Solid Earth Science',
        'title': 'European Plate Observing System',
        'acronym':'EPOS'
    },
    'eufar.net':{
        'id': 16,
        'url':'https://www.eufar.net/',
        'label': 'Atmospheric',
        'title': 'The EUropean Facility for Airborne Research',
        'acronym':'EUFAR'
    },
    'euro-argo.eu':{
        'id': 17,
        'url':'https://www.euro-argo.eu/',
        'label': 'Marine',
        'title': 'European Research Infrastructure Consortium for observing the Ocean',
        'acronym':'Euro-Argo ERIC'
    },
    'eurofleet.fr':{
        'id': 18,
        'url':'https://www.eurofleet.fr/',
        'label': 'Marine',
        'title': 'An alliance of European marine research infrastructure to meet the evolving needs of the research and industrial communities',
        'acronym':'EUROFLEETS+'
    },
    'eurogoos.eu':{
        'id': 19,
        'url':'https://eurogoos.eu/',
        'label': 'Marine',
        'title': 'European Global Ocean Observing System',
        'acronym':'EuroGOOS'
    },
    'eurochamp.org':{
        'id': 20,
        'url':'https://www.eurochamp.org/',
        'label': 'Atmospheric',
        'title': 'Integration of European Simulation Chambers for Investigating Atmospheric Processes',
        'acronym':'EUROCHAMP'
    },
    'hemera-h2020.eu':{
        'id': 21,
        'url':'https://www.hemera-h2020.eu/',
        'label': 'Atmospheric',
        'title': 'Integrated access to balloon-borne platforms for innovative research and technology',
        'acronym':'HEMERA'
    },
    'iagos.org':{
        'id': 22,
        'url':'https://www.iagos.org/',
        'label': 'Atmospheric',
        'title': 'In Service Aircraft for a Global Observing System',
        'acronym':'IAGOS'
    },
    'eu-interact.org':{
        'id': 23,
        'url':'https://eu-interact.org/',
        'label': 'Terrestrial Ecosystem',
        'title': 'Building Capacity For Environmental Research And Monitoring In Arctic And Neighbouring Alpine And Forest Areas',
        'acronym':'INTERACT'
    },
    'is.enes.org':{
        'id': 24,
        'url':'https://is.enes.org/',
        'label': 'Multi-domain',
        'title': 'Infrastructure For The European Network For Earth System Modelling Enes',
        'acronym':'IS-ENES'
    },
    'jerico-ri.eu':{
        'id': 25,
        'url':'https://www.jerico-ri.eu/',
        'label': 'Marine',
        'title': 'The European Integrated Infrastructure For In Situ Coastal Observation',
        'acronym':'JERICO-RI'
    },
    'sios-svalbard.org':{
        'id': 26,
        'url':'https://www.sios-svalbard.org/',
        'title': 'Multi-domain',
        'title': 'Svalbard integrated Earth observing system',
        'acronym':'SIOS'
    }
}


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
    "ResearchInfrastructure":{
        "terms":{
            "field": "ResearchInfrastructure.keyword",
            "size": 20,
        }
    },
    "file_extensions":{
        "terms":{
            "field": "file_extensions.keyword",
            "size": 20,
        }
    }
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
        "ResearchInfrastructure":getResearchInfrastructure(id[0])
    }
    res = es.index(index="webcontents", id= id, body=webFeatures)
    es.indices.refresh(index="webcontents")
#----------------------------------------------------------------------------------------------------------------------- envri-search-engine
def getResearchInfrastructure(url):
    lstRI=[]
    for RI in ResearchInfrastructures:
        if RI in url:
            if(ResearchInfrastructures[RI]['acronym'] not in lstRI):
                lstRI.append(ResearchInfrastructures[RI]['acronym'])
    return lstRI
#----------------------------------------------------------------------------------------------------------------------- envri-search-engine
def textCleansing(txt):
    if type(txt)==str:
        res = isinstance(txt, str)
        if res:
            txt=re.sub(r'[^A-Za-z0-9 .-\?/:,;~%$#*@!&+=_><]+', '', txt)
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
            index="webcontents",
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
            "from" : page,
            "size" : 10,
            "query": {
                "bool": {
                    "must": {
                        "multi_match" : {
                            "query": term,
                            "fields": [ "title", "text", "organizations", "publisher",
                                        "authors", "producers", "file_extensions", "locations",
                                        "ResearchInfrastructure"],
                            "type": "best_fields",
                            "minimum_should_match": "100%"
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


        result = es.search(index="webcontents", body=query_body)
    lstResults=[]
    for searchResult in result['hits']['hits']:
        searchResult['_source']['ResearchInfrastructure']= getResearchInfrastructure(searchResult['_source']['id'][0])
        lstResults.append(searchResult['_source'])

    #......................
    file_extensions=[]
    locations=[]
    producers=[]
    organizations=[]
    person=[]
    authors=[]
    ResearchInfrastructure=[]
    #......................
    for searchResult in result['aggregations']['ResearchInfrastructure']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!=""):
            RI={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            ResearchInfrastructure.append (RI)
    #......................
    for searchResult in result['aggregations']['locations']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!=""):
            loc={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            locations.append (loc)
    #......................
    for searchResult in result['aggregations']['producers']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!=""):
            prod={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            producers.append (prod)
    #......................
    for searchResult in result['aggregations']['organizations']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!=""):
            org={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            organizations.append (org)
    #......................
    for searchResult in result['aggregations']['person']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!=""):
            pers={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            person.append (pers)
    #......................
    for searchResult in result['aggregations']['authors']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!=""):
            auth={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            authors.append (auth)
    #......................
    for searchResult in result['aggregations']['file_extensions']['buckets']:
        if(searchResult['key']!="None" and searchResult['key']!="unknown" and searchResult['key']!="" and
                (searchResult['key']=="pdf") or (searchResult['key']=="doc")or (searchResult['key']=="xml") or (searchResult['key']=="xls") or (searchResult['key']=="txt")):
            ext={
                'key':searchResult['key'],
                'doc_count': searchResult['doc_count']
            }
            file_extensions.append (ext)
    #......................
    facets={
        "file_extensions":file_extensions,
        "locations":locations,
        "producers":producers,
        "organizations":organizations,
        "person":person,
        "authors":authors,
        "ResearchInfrastructure":ResearchInfrastructure
    }
    #envri-statics
    #print("Got %d Hits:" % result['hits']['total']['value'])
    #return JsonResponse(result, safe=True, json_dumps_params={'ensure_ascii': False})
    numHits=result['hits']['total']['value']

    upperBoundPage=round(np.ceil(numHits/10)+1)
    if(upperBoundPage>10):
        upperBoundPage=11

    return render(request,'webcontent_results.html',
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
