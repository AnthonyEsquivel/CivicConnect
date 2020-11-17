from django.forms import ModelForm
from mainapp.models import Template, Profile
from django.contrib.auth.models import User

class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = ['temp_name', 'temp_description', 'temp_text', 'tags', 'owner']

    # applying the css styling to the template name input box
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': "form-control"})
        # following line is for one item
        # self.fields['temp_name'].widget.attrs.update({'class': "form-control"})


#class EditProfileForm(ModelForm):
    #class Meta:
        #model = Profile
        #fields = ['location']

