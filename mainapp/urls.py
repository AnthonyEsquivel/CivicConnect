from django.urls import path

from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('createTemp/', views.makeTemplate, name='createTemp'),
    path('profile/', views.profile, name='profile'),
    path('browse/', views.browseTemplates, name='browse'),
    path("<int:id>", views.templatePage, name="templatePage"),
]