from django.urls import include, path
from . import views
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

app_name = 'mainapp'
urlpatterns = [
    path('', TemplateView.as_view(template_name="mainapp/index.html")),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('createTemp/', views.makeTemplate, name='createTemp'),
    path('profile/', views.profile, name='profile'),
]