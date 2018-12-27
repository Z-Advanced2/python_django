# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse

from .forms import ContactForm
from .mvalidate import Mvalidate

# Create your views here.

VALIDATE_RESULT = 'validation'
path = ""

def index(request):
    lists = ""
    current_objects = ""
    if request.method == 'POST':
        forms = ContactForm(request.POST)
        if forms.is_valid():
#            return HttpResponseRedirect('/Thanks/')
           VALIDATE_RESULT = forms.cleaned_data['path_inf']
           mvalidate = Mvalidate()
           lists = mvalidate.request(VALIDATE_RESULT)
         else:
            VALIDATE_RESULT = path
     else:
        forms = ContactForm()
        VALIDATE_RESULT = path
    validator_data = {
    'currentpath': VALIDATE_RESULT,
    'forms': forms,
    'lists': str(lists),
    }
    return render(request, 'validator/index.html', validator_data)
