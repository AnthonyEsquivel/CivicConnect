from django.shortcuts import  get_object_or_404, render, redirect
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
    userTemps = []
    for t in Template.objects.all():
        if t.owner == request.user:
            userTemps.append(t)
    return render(request, "mainapp/profile.html", context={
        'user': request.user,
        'userTemps': userTemps
    })


def makeTemplate(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            form.save()
        postName = request.POST.get("temp_name")
        postDesc = request.POST.get("temp_description")
        postTemp = request.POST.get("temp_text")
        newTemplate = Template(temp_name=postName, temp_description=postDesc, temp_text=postTemp,owner=request.user)
        newTemplate.save()
    return render(request, 'mainapp/createTemp.html', context={'form': TemplateForm})

def browseTemplates(request):
    publicTemps = []
    for t in Template.objects.all():
        if t.public:
            publicTemps.append(t)
    return render(request, "mainapp/browse.html", context={'templates': publicTemps})

def templatePage(request, id):
    template = get_object_or_404(Template, id=id)
    if request.method =='POST' and 'publish' in request.POST:
        template.public = True
        template.save(update_fields=["public"])
        return redirect('/profile')
    else:
        #Add share fuctionality
        send = "email" #placeholder (no functionality)

    return render(request, 'mainapp/tempPage.html', context= {'user':request.user,'template': template})
  
def logout_view(request):
    auth_logout(request)
    return redirect('')
    # Redirect to a success page.
