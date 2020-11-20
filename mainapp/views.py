from django.utils import timezone
from .models import Template, MyUser
import requests
import json
from django.shortcuts import  get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Template
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

def index(request):
    return render(request, "mainapp/index.html")


def news(request):
    return render(request, "mainapp/news.html")


def profile(request):
    userTemps = []
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

    # reference to user data on profile page (incase of empty form)
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
        'user': request.user,
        'userTemps': userTemps,
        "address": address})

    # final view render
    return render(request, "mainapp/profile.html", context={
        'user': request.user,
        'userTemps': userTemps,
        "address": address,
        "representatives": representatives,
        'test_representatives': test_representatives})

def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST['fname']
        request.user.last_name = request.POST['lname']
        if not hasattr(request.user, 'myuser'):
            request.user.myuser = MyUser(address=request.POST['address'], member_since=timezone.now())
        else:
            request.user.myuser.address = request.POST['address']
        request.user.myuser.save()
        request.user.save()
        return redirect('/profile')
    try:
        address = request.user.myuser.address
    except:
        address = '1826 University Ave, Charlottesville, VA 22904'
    return render(request, "mainapp/editProfile.html", context= {'user':request.user,"address": address})

def makeTemplate(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            form.save()
        postName = request.POST.get("temp_name")
        postDesc = request.POST.get("temp_description")
        postTemp = request.POST.get("temp_text")
        newTemplate = Template(temp_name=postName, temp_description=postDesc, temp_text=postTemp, owner=request.user)
        newTemplate.save()
        return redirect('/profile')
    return render(request, 'mainapp/createTemp.html', context={'form': TemplateForm})
    
def browseTemplates(request):
    queryset = Template.objects.all().order_by('-pub_date').filter(is_approved=True)
    publicTemps = []
    for q in queryset:
        if q.public:
            publicTemps.append(q)
    return render(request, "mainapp/browse.html", context={'templates': publicTemps})


def templatePage(request, id):
    template = get_object_or_404(Template, id=id)
    if request.method == 'POST' and 'publish' in request.POST:
        template.public = True
        template.save(update_fields=["public"])
        return redirect('/profile')
    else:
        #Add share functionality
        if request.method == 'POST' and 'send' in request.POST:
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
                                                              'test_representatives': test_representatives})

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



