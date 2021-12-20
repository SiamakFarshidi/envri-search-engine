from django.shortcuts import render
import glob
from os.path import isfile, join
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Index
import os
from os import walk
import json
import uuid

#-----------------------------------------------------------------------------------------------------------------------
def aggregates(request):

    return  0
#-----------------------------------------------------------------------------------------------------------------------
def genericsearch(request):
    return  0
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
            res = es.index(index="webapi", id= uuid.uuid4(), body=indexfile)
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
