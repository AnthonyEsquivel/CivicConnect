from django.shortcuts import render
from django.http import HttpResponse
from .models import Template
from .forms import TemplateForm
from django.contrib.auth import logout


# Create your views here.

# Getting the data from the model and pass it to the template
# You can also get data from the template and put it into the model

def index(request):
    return render(request, "mainapp/index.html")

def news(request):
    return render(request, "mainapp/news.html")

def profile(request):
    return render(request, "mainapp/profile.html", context={
        'user': request.user,
        'templates': Template.objects.all()
    })


def makeTemplate(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            form.save()
        postName = request.POST.get("temp_name")
        postDesc = request.POST.get("temp_description")
        postTemp = request.POST.get("temp_text")
        newTemplate = Template(temp_name=postName, temp_description=postDesc, temp_text=postTemp)
        newTemplate.save()
    return render(request, 'mainapp/createTemp.html', context={'form': TemplateForm})

def logout_view(request):
    auth_logout(request)
    return redirect('')
    # Redirect to a success page.
