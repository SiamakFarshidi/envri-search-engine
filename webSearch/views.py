from django.shortcuts import render

# Create your views here.
def uploadFromJsonLibrary(request):
    print("indexing...")


    response_data = {}
    response_data['result'] = ""
    response_data['message'] = 'The indexing process of the  dataset repository has been initiated!'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

#----------------------------------------------------------------------------------------------------------------------- envri-search-engine
def aggregates(request):
    print("indexing...")


    response_data = {}
    response_data['result'] = ""
    response_data['message'] = 'The indexing process of the dataset repository has been initiated!'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

#-----------------------------------------------------------------------------------------------------------------------
def genericsearch(request):
    print("indexing...")


    response_data = {}
    response_data['result'] = ""
    response_data['message'] = 'The indexing process of the dataset repository has been initiated!'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

