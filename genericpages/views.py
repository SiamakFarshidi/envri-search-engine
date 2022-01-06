from django.shortcuts import render

# Create your views here.

def landingpage(request):
    return render(request,'landingpage.html',{})

def genericpages(request):

    try:
        page = request.GET['page']
    except:
        page = ''

    if page=="publications":
        return render(request,'publications.html',{})
    elif page=="RnD":
        return render(request,'RnDTeam.html',{})
    elif page=="graphV":
        return render(request,'graphBasedVisualization.html',{})
    elif page=="home":
        request.session['filters']=[]
        return render(request,'landingpage.html',{})

