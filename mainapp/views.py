# /***************************************************************************************
# *  REFERENCES
# *  Title: The admin approval backend
# *  Author: James Bennett, Andrew Cutler, and others.
# *  Date: 2007-2017
# *  Code version: N/A
# *  URL: https://django-registration-redux.readthedocs.io/en/latest/admin-approval-backend.html
# *  Software License: N/A (None specified)
# * 
# * Title: What You Need to Know to Manage Users in Django Admin
# * Author: Haki Benita
# * Date: Not specified
# * Code version: N/A
# * URL: https://realpython.com/manage-users-in-django-admin/
# * Software License: N/A (None specified)
# *
# * Title: Google Civic Information API 
# * Author: N/A
# * Date: Not specified
# * Code version: N/A
# * URL: https://developers.google.com/civic-information
# * Software License: Apache 2.0
# ***************************************************************************************/
from django.utils import timezone
from .models import Template, MyUser, Tags
import requests
import json
from django.shortcuts import  get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import TemplateForm
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

# Create your views here.

# Getting the data from the model and pass it to the template
# You can also get data from the template and put it into the model

# google api key
key = "AIzaSyAqg74M90_V9eS2j06NNzGK-PqRNZ9sbLg"

#Creating Tags
tags = ['Climate Change', 'Racial Justice', 'Health Care','Student Debt','Foreign Policy','Policing','Gun Policy','Animal Rights','LGBTQ+']
'''
for i in range(len(Tags.objects.all()),len(tags)-1):
    t = Tags(name=tags[i+1],id=i+1)
    t.save()
    print(i)
'''
if len(Tags.objects.all()) != len(tags):
    t1 = Tags(name='Climate Change',id=1)
    t1.save()
    t2 = Tags(name='Racial Justice',id=2)
    t2.save()
    t3 = Tags(name='Health Care',id=3)
    t3.save()
    t4 = Tags(name='Student Debt',id=4)
    t4.save()
    t5 = Tags(name='Foreign Policy',id=5)
    t5.save()
    t6 = Tags(name='Policing',id=6)
    t6.save()
    t7 = Tags(name='Gun Policy',id=7)
    t7.save()
    t8 = Tags(name='Animal Rights',id=8)
    t8.save()
    t9 = Tags(name='LGBTQ+',id=9)
    t9.save()


def index(request):
    return render(request, "mainapp/index.html")


def news(request):
    return render(request, "mainapp/news.html")


def profile(request):
    #print("hello", request.user.myuser)
    userTemps = []
    if request.user.is_staff==True:
        for t in Template.objects.all():
            if t.public == False:
                userTemps.append(t)
    else:
        for t in Template.objects.all():
            if t.owner == request.user:
                userTemps.append(t)

    # grab representatives based on address and API key --------------------------------------------------------------

    if request.method == 'POST' and 'representatives' in request.POST:
        # create a new user w an address
        if not hasattr(request.user, 'myuser'):
            # make user address whatever person types into form
            request.user.myuser = MyUser(address=request.POST['address'], member_since=timezone.now())
        # update an existing user address
        else:
            request.user.myuser.address = request.POST['address']
        # request.user.myuser.address = request.POST['address']
        request.user.myuser.save()
    try:
        issues = request.user.myuser.issues.all()
        if len(issues) == 0:
            issues = ["Go to edit profile to add issues that are important to you"]
    except:
        issues = ['No Issues']
    # reference to user data on profile page (incase of empty form)
    try:
        address = request.user.myuser.address
        print(address)
    except:
        # imitation address for checking
        address = '1826 University Ave, Charlottesville, VA 22904'

    try:
        url = f"https://civicinfo.googleapis.com/civicinfo/v2/representatives?address={address}&includeOffices=true&key={key}"
        response = requests.get(url)

        representatives = response.json()

        json_reps = json.loads(response.text)
        offices = json_reps['offices']

        officials = json_reps['officials']
        test_representatives = {}

        for official_idx, official in enumerate(officials):
            test_representatives[official_idx] = official
            for office_idx, office in enumerate(offices):
                if official_idx in office['officialIndices']:
                    test_representatives[official_idx]['office'] = office

    except KeyError:
        # send back to profile we write error message
        return render(request, "mainapp/profile.html", context={
        'user': request.user,
        'userTemps': userTemps,
        "address": address})

    # final view render
    return render(request, "mainapp/profile.html", context={
        'user': request.user,
        'userTemps': userTemps,
        "address": address,
        "issues":issues,
        "representatives": representatives,
        'test_representatives': test_representatives})

def edit_profile(request):
    issues = tags
    if request.method == 'POST':
        request.user.first_name = request.POST['fname']
        request.user.last_name = request.POST['lname']
        if not hasattr(request.user, 'myuser'):
            request.user.myuser = MyUser(address=request.POST['address'], member_since=timezone.now())
        else:
            request.user.myuser.address = request.POST['address']
        #Tag feature adds issues to users tags
        i = 0
        for tag in issues:
            i += 1
            if tag in request.POST:
                t = get_object_or_404(Tags, id=i)
                if t in request.user.myuser.issues.all():
                    request.user.myuser.issues.remove(t)
                else:
                    request.user.myuser.issues.add(t)

        request.user.myuser.save()
        request.user.save()
        return redirect('/profile')
    try:
        address = request.user.myuser.address
    except:
        address = '1826 University Ave, Charlottesville, VA 22904'
    return render(request, "mainapp/editProfile.html", context= {'user':request.user,"address": address, 'issues':issues})

def makeTemplate(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            form.save()
        postName = request.POST.get("temp_name")
        postDesc = request.POST.get("temp_description")
        postTemp = request.POST.get("temp_text")
        newTemplate = Template(temp_name=postName, temp_description=postDesc, temp_text=postTemp, owner=request.user, is_submittedForReview=True)
        newTemplate.save()
        i = 0
        for tag in tags:
            i += 1
            if tag in request.POST:
                t = get_object_or_404(Tags, id=i)
                newTemplate.tags.add(t)
        newTemplate.save()
        return redirect('/profile')
    return render(request, 'mainapp/createTemp.html', context={'form': TemplateForm, 'tags':tags})

def browseTemplates(request):
    queryset = Template.objects.all().order_by('-pub_date').filter(public=True)
    publicTemps = []
    for q in queryset:
        if q.public:
            publicTemps.append(q)
    return render(request, "mainapp/browse.html", context={'templates': publicTemps})


def templatePage(request, id):
    template = get_object_or_404(Template, id=id)
    tags = template.tags.all()
    if len(tags) == 0:
        tags =["None"]
    if request.method == 'POST' and 'publish' in request.POST:
        template.public = True
        template.is_approved = True
        template.is_submittedForReview = False
        template.save(update_fields=["public"])
        return redirect('/profile')
    else:
        #Add share functionality
        if request.method == 'POST' and 'send' in request.POST:
            print(request.POST)
            form = ContactForm(request.POST)
            if 'radios' in request.POST:
                email = request.POST['radios']
                print(email)
            if form.is_valid():
                subject = request.POST.get('subject')
                if request.POST.get('to_email'):
                    email = request.POST.get('to_email')
                message = request.POST.get('message')
                try:
                    send_mail(subject, message,'civicconnect112@gmail.com', [email])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('/success')

    # getting address and representatives-----------------------------------------------------
    try:
        address = request.user.myuser.address
    except:
        # imitation address for checking
        address = '1826 University Ave, Charlottesville, VA 22904'

    try:
        url = f"https://civicinfo.googleapis.com/civicinfo/v2/representatives?address={address}&includeOffices=true&key={key}"
        response = requests.get(url)
        representatives = response.json()
        json_reps = json.loads(response.text)
        offices = json_reps['offices']
        officials = json_reps['officials']
        test_representatives = {}

        for official_idx, official in enumerate(officials):
            test_representatives[official_idx] = official
            for office_idx, office in enumerate(offices):
                if official_idx in office['officialIndices']:
                    test_representatives[official_idx]['office'] = office

    except KeyError:
        # send back to profile we write error message
        return render(request, "mainapp/profile.html", context={
        'user': request.user})

    # final view
    return render(request, 'mainapp/tempPage.html', context= {'user':request.user,
                                                              'template': template,
                                                              'form': ContactForm, "address": address,
                                                              "representatives": representatives,
                                                              'test_representatives': test_representatives,
                                                              'tags':tags})

def logout_view(request):
    # commented out bc it was an error
    # auth_logout(request)
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
