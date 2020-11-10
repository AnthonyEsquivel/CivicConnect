from django.shortcuts import  get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Template
from .forms import TemplateForm
from django.contrib.auth import logout
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

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

def browseTemplates(request):
    return render(request, "mainapp/browse.html", context={'templates': Template.objects.all()})

def templatePage(request, id):
    template = get_object_or_404(Template, id=id)
    #template = Template.objects.get(id=id)
    return render(request, 'mainapp/tempPage.html', context= {'template': template})

def logout_view(request):
    auth_logout(request)
    return redirect('')
    # Redirect to a success page.

def sendEmail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = request.POST.get('subject')
            to_email = request.POST.get('to_email')
            message = request.POST.get('message')
            try:
                send_mail(subject, message,'civicconnect112@gmail.com', [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('/success')
    return render(request, 'mainapp/sendEmail.html', context={'form': ContactForm})

def successView(request):
    return render(request, "mainapp/success.html")
