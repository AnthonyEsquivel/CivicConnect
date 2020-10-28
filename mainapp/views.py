from django.shortcuts import render
from django.http import HttpResponse
from .models import Template
from django.contrib.auth import logout

# Create your views here.
def index(request):
    return render(request, "mainapp/index.html")

def profile(request):
    return render(request, "mainapp/profile.html")

def makeTemplate(request):
    if request.method == 'POST':
        postName = request.POST.get("temp_name")
        postDesc = request.POST.get("temp_description")
        postTemp = request.POST.get("temp_text")
        newTemplate = Template(temp_name = postName, temp_description=postDesc, temp_text=postTemp)
        newTemplate.save()
    return render(request, 'mainapp/createTemp.html')


def logout_view(request):
    auth_logout(request)
    return redirect('')
    # Redirect to a success page.
