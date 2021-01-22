from django.shortcuts import render, redirect
from django.http import HttpResponse
from .module import chopin_model
from music21 import *
from django.views import generic
from .forms import SingleUploadForm
from pathlib import Path
from django.template import loader

relative_path = Path(__file__).resolve().parent.parent

class chopin_form_upload(generic.FormView):
    form_class = SingleUploadForm
    template_name = 'chopin/index.html'

    def form_valid(self, form):
        download_url = str(relative_path) + form.save()
        score = chopin_model.Chopin_NeuralNetwork(download_url)
        print(score)
        if score != None:
            score.write("Midi", fp=str(relative_path) + '/media/documents/MIDI.mid')
            score.write("MusicXML", fp=str(relative_path) + '/media/documents/document.xml')
            context = {
                'score': score,
            }
            return self.render_to_response(context)
        else:
            context = {
                'flag': "対応していないファイルです",
            }
            return self.render_to_response(context)

def make_xml(request):
    return render(request, 'chopin/make_xmlfile.html')

def model(request):
    return render(request, 'chopin/model.html')

def samplemusic(request):
    return render(request, 'chopin/samplemusic.html')