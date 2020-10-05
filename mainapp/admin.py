from django.contrib import admin
from .models import Template

# Register your models here.
class TemplateAdmin(admin.ModelAdmin):
    model = Template
admin.site.register(Template)