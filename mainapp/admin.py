from django.contrib import admin
from .models import Template
from .models import MyUser


# Register your models here.
class TemplateAdmin(admin.ModelAdmin):
    model = Template
admin.site.register(Template)
admin.site.register(MyUser)

