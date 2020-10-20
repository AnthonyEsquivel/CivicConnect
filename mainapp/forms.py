from django.forms import ModelForm
from mainapp.models import Template

class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = ['temp_name', 'temp_description', 'temp_text', 'tags', 'owner']
