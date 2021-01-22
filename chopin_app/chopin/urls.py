from django.urls import path

from . import views

app_name = 'chopin'

urlpatterns = [
    path('upload', views.chopin_form_upload.as_view(), name='upload'),
    path('xml', views.make_xml, name='xml'),
    path('model', views.model, name='model'),
    path('samplemusic', views.samplemusic, name='samplemusic'),
]