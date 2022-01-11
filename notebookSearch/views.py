from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json
from github import Github
from urllib.request import urlopen
import urllib
from github import RateLimitExceededException
import shlex
import subprocess
import requests
import gitlab
import os
import time
import pandas as pd
import re
#-------------------------------------------------------------------------------------------
ACCESS_TOKEN_Github= "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"
ACCESS_TOKEN_Gitlab= "glpat-RLNz1MhmyeR7jcox_dyA"

# http request authentication
header = {"Authorization": "token %s" % ACCESS_TOKEN_Github}
# initialize query request parameters
base_url = 'https://api.github.com/search/code?l=Jupyter+Notebook&q=ipynb+in:path+extension:ipynb'
page_url = '&per_page=100'
indexPath="/var/lib/opensemanticsearch/notebookSearch/Indexes.json"
#-------------------------------------------------------------------------------------------
def genericsearch(request):
    try:
        term = request.GET['term']
    except:
        term = ''
    response_data= {}

    if (term=="*"):
        term=""
    #response_data= search_github_by_url(term)
    response_data=search_repository_github(term)
    #search_projects_Gitlab(term)

    return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request,'notebook_results.html',response_data)

#-------------------------------------------------------------------------------------------
def search_projects_Gitlab(keyword):
    #    cURL = r'curl --header "PRIVATE-TOKEN:'+ACCESS_TOKEN_Gitlab+'" "https://gitlab.example.com/api/v4/search?scope=projects&search='+keyword+'"'
    gl = gitlab.Gitlab('https://gitlab.com/', private_token=os.getenv(ACCESS_TOKEN_Gitlab))
    gl.search(gitlab.SEARCH_SCOPE_ISSUES, keyword, page=2, per_page=10)

    # get a generator that will automatically make required API calls for
    # pagination
    for item in gl.search(gitlab.SEARCH_SCOPE_ISSUES, search_str, as_list=False):
        print(item)

    json_data={}
    return json_data
#-------------------------------------------------------------------------------------------

def search_repository_github(keywords):
    g = Github(ACCESS_TOKEN_Github)
    keywords = [keyword.strip() for keyword in keywords.split(',')]
    keywords.append("notebook")
    query = '+'.join(keywords)+ '+in:readme+in:description'
    result = g.search_repositories(query, 'stars', 'desc')
    cnt=0
    data=[]
    iter_obj = iter(result)
    while True:
        try:
            cnt=cnt+1
            repo = next(iter_obj)
            new_record= {
                "id":cnt,
                "name": repo.full_name,
                "description": re.sub(r'[^A-Za-z0-9 ]+', '',repo.description),
                "html_url":repo.html_url,
                "git_url": repo.clone_url,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "size": repo.size,
            }
            if new_record["language"]=="Jupyter Notebook" and new_record not in data:
                data.append(new_record)
        except StopIteration:
            break
        except RateLimitExceededException:
            continue
    data=(json.dumps({"results_count": result.totalCount,"hits":data}).replace("'",'"'))
    return  json.loads(data)
#-------------------------------------------------------------------------------------------
def github_index_pipeline(request):
    g = Github(ACCESS_TOKEN_Github)
    keywords = [keyword.strip() for keyword in keywords.split(',')]
    keywords.append("Jupyter Notebook")
    query = '+'.join(keywords) + '+in:readme+in:description'
    result = g.search_repositories(query, 'stars', 'desc')
    cnt=0
    data=[]
    iter_obj = iter(result)
    while True:
        try:
            cnt=cnt+1
            repo = next(iter_obj)
            new_record= {
                "id":cnt,
                "name": repo.full_name,
                "html_url":repo.html_url,
                "git_url": repo.clone_url,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "size": repo.size,
            }
            if new_record["language"]=="Jupyter Notebook" and new_record not in data:
                data.append(new_record)
        except StopIteration:
            break
        except RateLimitExceededException:
            search_rate_limit = g.get_rate_limit().search
            logger.info('search remaining: {}'.format(search_rate_limit.remaining))
            reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())
            # add 10 seconds to be sure the rate limit has been reset
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 10
            time.sleep(sleep_time)
            continue
    indexFile= open(indexPath,"w+")
    indexFile.write(data)
    indexFile.close()
    return  "Github indexing finished!"
#-------------------------------------------------------------------------------------------
def search_code_github(keyword):
    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} API calls remaining. Reset time: {rate.reset}')
        return
    else:
        print(f'You have {rate.remaining}/{rate.limit} API calls remaining')

    query = f'"{keyword} english" in:file extension:po'
    result = g.search_code(query, order='desc')

    max_size = 100
    print(f'Found {result.totalCount} file(s)')
    if result.totalCount > max_size:
        result = result[:max_size]

    for file in result:
        print(f'{file.download_url}')

#-------------------------------------------------------------------------------------------
def search_repository_github_by_url(keywords):
    query='https://api.github.com/search/repositories?q='+keywords

    request = urllib.request.urlopen(query)
    data = json.load(request)
    return data
#-------------------------------------------------------------------------------------------
