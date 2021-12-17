from __future__ import print_function
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
import json
from urllib.request import urlopen
import pysolr
import string
import random # define the random module
from urllib.parse import quote
import simplejson

#--------------------------------------------------------------
coreName = 'opensemanticsearch'
URL = 'http://localhost:8983/solr/'
#--------------------------------------------------------------
def processSingleReq(request):
    FeatureID = request.GET["ID"]
    FeatureReq = request.GET["Req"] # MoSCoW

    return HttpResponse(FeatureID+" >< "+FeatureReq)
# --------------------------------------------------------------
def processReqFile(request):
    result="{id:123}"
    return HttpResponse(json.dumps({'queue': result.id}), content_type="application/json")
# --------------------------------------------------------------
def index(request):
    return JsonResponse({"hello":"pythonist"})
# -------------------------------------------------------------- Metadata
realstate_qualities_metadata={
    "suitability":{
        "metadata": {
            "type": "string",
            "quality": ["null"],
            "description": "desc",
        },
    },
    "popularity":{
        "metadata": {
            "type": "string",
            "quality": ["null"],
            "description": "desc",
        },
    },
    "locality": {
        "metadata": {
            "type": "string",
            "quality": ["null"],
            "description": "desc",
        },
    },
    "accessibility":{
        "metadata": {
            "type": "string",
            "quality": ["null"],
            "description": "desc",
        },
    },
    "safety":{
        "metadata": {
            "type": "string",
            "quality": ["null"],
            "description": "desc",
        },
    },
}
realstate_features_metadata={
    "id": {
        "metadata": {
            "type": "string",
            "quality": ["null"],
            "description": "desc",
        },
    },
    "place": {
        "metadata": {
            "type": "list",
            "quality": ["suitability", "popularity", "locality", "accessibility", "safety"],
            "description": "desc",
        },
        "address": {
            "metadata": {
                "type": "list",
                "quality": ["suitability", "popularity", "locality", "accessibility", "safety"],
                "description": "desc",
            },
            "street": {
                "metadata": {
                    "type": "string",
                    "quality": ["popularity", "locality", "accessibility", "safety"],
                    "description": "desc",
                },
            },
            "houseNumber": {
                "metadata": {
                    "type": "string",
                    "quality": [ "locality"],
                    "description": "desc",
                },
            },
            "zipCode": {
                "metadata": {
                    "type": "string",
                    "quality": ["locality", "accessibility"],
                    "description": "desc",
                },
            },
            "city": {
                "metadata": {
                    "type": "string",
                    "quality": ["suitability", "popularity", "locality", "accessibility", "safety"],
                    "description": "desc",
                },
            },
            "country": {
                "metadata": {
                    "type": "string",
                    "quality": ["null"],
                    "description": "desc",
                },
            },
        },
        "geolocation": {
            "metadata": {
                "type": "list",
                "quality": ["null"],
                "description": "desc",
            },
            "lat":{
                "metadata": {
                    "type": "number",
                    "quality": ["null"],
                    "description": "desc",
                },
            },
            "lng": {
                "metadata": {
                    "type": "number",
                    "quality": ["null"],
                    "description": "desc",
                },
            },
        }
    },
    "image": {
        "metadata": {
            "type": "string",
            "quality": ["null"],
            "description": "desc",
        },
        "url": {
            "metadata": {
                "type": "string",
                "quality": ["null"],
                "description": "desc",
            },
        },
    },
    "price": {
            "metadata": {
                "type": "monetary",
                "quality": ["null"],
                "description": "desc",
            },
        },
    "environment": {
            "metadata": {
                "type": "string",
                "quality": ["null"],
                "description": "desc",
            },
        },
    "rooms":{
            "metadata": {
                "type": "number",
                "quality": ["null"],
                "description": "desc",
            },
        },
    "rank": {
            "metadata": {
                "type": "number",
                "quality": ["null"],
                "description": "desc",
            },
        },
    "livingArea": {
            "metadata": {
                "type": "number",
                "quality": ["null"],
                "description": "desc",
            },
        },
    "plotArea":{
            "metadata": {
                "type": "number",
                "quality": ["null"],
                "description": "desc",
            },
        },
    "kindOfHouse": {
            "metadata": {
                "type": "string",
                "quality": ["null"],
                "description": "desc",
            },
        },
    "energyLabel": {
            "metadata": {
                "type": "string",
                "quality": ["null"],
                "description": "desc",
            },
        },
    "constructionYear": {
            "metadata": {
                "type": "date",
                "quality": ["null"],
                "description": "desc",
            },
        },
    "suitableFor": {
            "metadata": {
                "type": "string",
                "quality": ["null"],
                "description": "desc",
            },
        },
}
#--------------------------------------------------------------
def score_calculation():
    j1={
        "id": get_random_string(10),
        "place": {
            "address": {
                "street": "Wildebeest",
                "houseNumber": "25",
                "zipCode": "1011 NH",
                "city": "Amsterdam",
                "country": "Nederland"
            },
            "geolocation": {
                "lat": "52.36884694929380",
                "lng": "4.903875527379068"
            }
        },
        "image": {
            "url": "https://cloud.funda.nl/valentina_media/140/940/542_2160.jpg",
        },
        "price": 675.00,
        "environment": "busy",
        "rooms": 2,
        "rank": 99,
        "livingArea": 215,
        "plotArea": 730,
        "kindOfHouse": "appartment",
        "energyLabel": "D",
        "constructionYear": 1934,
        "suitableFor": "single"
    }

    j2={
        "id": get_random_string(10),
        "place": {
            "address": {
                "street": "Wildebeest",
                "houseNumber": "25",
                "zipCode": "1011 NH",
                "city": "Amsterdam",
                "country": "Nederland"
            },
            "geolocation": {
                "lat": "52.36884694929380",
                "lng": "4.903875527379068"
            }
        },
        "image": {
            "url": "https://cloud.funda.nl/valentina_media/140/940/542_2160.jpg",
        },
        "price": 675.00,
        "environment": "busy",
        "rooms": 2,
        "rank": 99,
        "livingArea": 215,
        "plotArea": 730,
        "kindOfHouse": "appartment",
        "energyLabel": "D",
        "constructionYear": 783,
        "suitableFor": "single"
    }

    extractValues(j1,j2)

    return 0
# --------------------------------------------------------------
def extractValues(requirements,solution):
    for key, value in solution.items():
        if key in requirements and requirements[key]!="":
            print (requirements[key])
        print (key, value)
        if isinstance(value, dict):
            extractValues(requirements[key],value)
    return 0
# --------------------------------------------------------------

HardContraints=""
SoftContraints=""

def GetQuery(Requirements):
    global HardContraints
    global SoftContraints
    HardContraints=""
    SoftContraints=""
    QueryGenerator(Requirements)
    if(HardContraints!="" and SoftContraints!=""):
        Query= "("+HardContraints+") AND ("+SoftContraints+" OR *:*)"
    elif(HardContraints!="" and SoftContraints==""):
        Query=HardContraints;
    else:
        Query=SoftContraints + " OR *:*";
    print (Query)
    return Query
# --------------------------------------------------------------
def QueryGenerator(Requirements):
    global HardContraints
    global SoftContraints

    for key,value in Requirements.items():
        if type(value) !=type(list()) or type(value) !=type(dict()):
            #print (str(key)+'---->'+str(value))

            if str(value)[0:1]=="M":
                if HardContraints!="":
                    HardContraints=HardContraints+' AND '+  str(key) + ' :"'+ str(value)[2:]+'"'
                else:
                    HardContraints= str(key)  + ' :'+ str(value)[2:]+''
            elif str(value)[0:1]=="S" or str(value)[0:1]=="C":
                if SoftContraints!="":
                    SoftContraints=SoftContraints+' OR '+  str(key) + ' :"'+ str(value)[2:]+'"'
                else:
                    SoftContraints= str(key) + ' :"'+ str(value)[2:]+'"'

        if type(value) == type(dict()):
            QueryGenerator(value)
        elif type(value) == type(list()):
            for val in value:
                if type(val) == type(str()):
                    pass
                elif type(val) == type(list()):
                    pass
                else:
                    QueryGenerator(val)

# --------------------------------------------------------------
def count(request):
    FeatureReq=request.POST.get('FeatureReq')
    data = json.loads(FeatureReq)
    query = GetQuery(data[0])
    data = searchSolr_getCount(query)
    print(data)
    data=[{"count":data}]
    return HttpResponse(json_data, content_type="application/json")
# --------------------------------------------------------------
def home(request):

    if request.method == 'POST':

        #FeatureReq=request.POST.get('FeatureReq')
        #data = json.loads(FeatureReq)

        print("okay")

        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            FeatureReq=request.POST.get('FeatureReq')
            data = json.loads(FeatureReq)
            connectToSolr()
            type=data[0]['callType']

            #print(data[0])
            #query="*:*" # all docs
            #query='kindOfHouse:"appartment"  AND price: 675.0'



            if(type=="list"):
                query = GetQuery(data[0])
                data = searchSolr_getList(query)

            elif(type=="count"):
                query = GetQuery(data[0])
                data = searchSolr_getCount(query)
                print(data)
                data=[{"count":data}]

            elif(type=="detail"):
                query ='id:'+'"'+data[0]['id']+'"'
                data = searchSolr(query)

            #score_calculation()
#            addDocumentSolr()
            #checkDifference()


            #printSolr(searchSolr(query))

            #print(fasetSearch (query,'capacity'))
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type="application/json")
            #return JsonResponse(data, safe=False)
    #Get goes here
    return render(request,'base.html')
# --------------------------------------------------------------
def addNew(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            NewAlternative=request.POST.get('NewAlternative')
            data = json.loads(NewAlternative)
            connectToSolr()
            #print(NewAlternative)
            addDocumentSolr(data)


    return render(request,'addNewAlternative.html')
# --------------------------------------------------------------
def printSolr(searchResults):
    for document in searchResults:
        print("  id :", document['id'])
# --------------------------------------------------------------
def connectToSolr():
    global coreName
    global URL

    if checkSolrCoreExistance(URL,coreName)==0: #################### Create new core
        connection = urlopen(URL+'admin/cores?action=CREATE&name='+coreName+'&instanceDir=./&config=solrconfig.xml&dataDir=data')
        response = json.load(connection)
        #print(response['response'])
# --------------------------------------------------------------
def checkSolrCoreExistance(URL,core):
    connection = urlopen(URL+'admin/cores?action=STATUS&core='+core)
    response = json.load(connection)
    if ( len(response['status'][core])==0):
        return 0
    return 1
# --------------------------------------------------------------
def fasetSearch(query,field):
    global coreName
    global URL
    solr = pysolr.Solr(URL+coreName)
    result = solr.search(query, **{
        'fl': 'content',
        'facet': 'true',
        'facet.field': field
    })

    return result.facets
# --------------------------------------------------------------
def searchSolr(query):
    global coreName
    global URL
    solr = pysolr.Solr(URL+coreName, always_commit=True, timeout=100)
    response = solr.search(query)
    return (response.docs)
# --------------------------------------------------------------
def searchSolr_getCount(query):
    global coreName
    global URL
    solr = pysolr.Solr(URL+coreName, always_commit=True, timeout=100)
    response = solr.search(query)
    return (response.hits)
# --------------------------------------------------------------
def searchSolr_getList(query):
    global coreName
    global URL

    solr = pysolr.Solr(URL+coreName, always_commit=True, timeout=100)
    response = solr.search(query,fl='id,place,rank,image')
    #similar = solr.more_like_this(q='id:doc_2', mltfl='text')
    return (response.docs)
# --------------------------------------------------------------
def addDocumentSolr(newDoc):
    global coreName
    global URL
    solr = pysolr.Solr(URL+coreName)

    solr.add(newDoc)
    print("added")

# --------------------------------------------------------------
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
