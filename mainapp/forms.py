# /***************************************************************************************
# *  REFERENCES
# *  Title: Django Email/Contact Form Tutorial
# *  Author: Will Vincent
# *  Date:  Nov 10, 2020
# *  Code version: 3.0
# *  URL: https://learndjango.com/tutorials/django-email-contact-form#create-forms
# *  Software License: MIT
# ***************************************************************************************/

from django.forms import ModelForm
from mainapp.models import Template
from django import forms


class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = ['temp_name', 'temp_description', 'temp_text', 'tags', 'owner']

    # applying the mainapp styling to the template name input box
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': "form-control"})
        # following line is for one item
        # self.fields['temp_name'].widget.attrs.update({'class': "form-control"})

class ContactForm(forms.Form):
    to_email = forms.EmailField(required=False)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
