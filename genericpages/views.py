from django.shortcuts import render

# Create your views here.

def genericpages(request):

    try:
        page = request.GET['page']
    except:
        page = ''

    if page=="publications":
        return render(request,'publications.html',{})
    elif page=="RnD":
        return render(request,'RnDTeam.html',{})
