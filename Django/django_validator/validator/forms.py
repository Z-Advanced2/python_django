# -*- coding: utf-8 -*-
from django import forms

class ContactForm(forms.Form):
    path_inf = forms.CharField(label='Path Infomation', max_length=1000)
