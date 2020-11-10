from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Template
from .forms import TemplateForm
import requests
import json
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
        newTemplate = Template(temp_name=postName, temp_description=postDesc, temp_text=postTemp, owner=request.user)
        newTemplate.save()
        return redirect('/profile')
    return render(request, 'mainapp/createTemp.html', context={'form': TemplateForm})


def browseTemplates(request):
    publicTemps = []
    for t in Template.objects.all().order_by('-pub_date'):
        if t.public:
            publicTemps.append(t)
    return render(request, "mainapp/browse.html", context={'templates': publicTemps})


def templatePage(request, id):
    template = get_object_or_404(Template, id=id)
    if request.method == 'POST' and 'publish' in request.POST:
        template.public = True
        template.save(update_fields=["public"])
        return redirect('/profile')
    else:
        # Add share fuctionality
        send = "email"  # placeholder (no functionality)

    return render(request, 'mainapp/tempPage.html', context={'user': request.user, 'template': template})

def logout_view(request):
    # commented out bc it was an error
    # auth_logout(request)
    return redirect('')
    # Redirect to a success page.

# grab representatives based on address and API key
def get_data(request):
    address = request.POST['address']
    key = "AIzaSyAqg74M90_V9eS2j06NNzGK-PqRNZ9sbLg"
    if request.method == 'POST' and 'representatives' in request.POST:
        try:
            url = f"https://civicinfo.googleapis.com/civicinfo/v2/representatives?address={address}&includeOffices=true&key={key}"
            response = requests.get(url)
            representatives = response.json()
            json_reps = json.loads(response.text)
            offices = json_reps['offices']
            officials = json_reps['officials']
            names = []
            indices = []
            test_representatives = {}
            print(type(officials))

            for official_idx, official in enumerate(officials):
                test_representatives[official_idx] = official
                for office_idx, office in enumerate(offices):
                    if official_idx in office['officialIndices']:
                        test_representatives[official_idx]['office'] = office

            dict_items = test_representatives.items()
            return render(request, "mainapp/profile.html", {"address": address, "representatives": representatives, 'test_representatives': test_representatives})

        except KeyError:
            # send to random page until we write error message
            return render(request, "mainapp/news.html")
    return

