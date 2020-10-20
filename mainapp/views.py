from django.shortcuts import render
from django.http import HttpResponse
from .models import Template


# Create your views here.

def index(request):
    return render(request, "mainapp/index.html")


def profile(request):
    return render(request, "mainapp/profile.html", context={
        'user': request.user,
        'templates': Template.objects.all()
    })


def makeTemplate(request):
    if request.method == 'POST':
        print(request.POST)
        postName = request.POST.get("temp_name")
        postDesc = request.POST.get("temp_description")
        postTemp = request.POST.get("temp_text")
        print(postTemp)
        newTemplate = Template(temp_name=postName, temp_description=postDesc, temp_text=postTemp)
        newTemplate.save()
    return render(request, 'mainapp/createTemp.html')
