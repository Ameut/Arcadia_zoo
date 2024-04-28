from django import forms
from .models import Avis
from .models import Contact
from django.contrib import admin


class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['pseudo', 'commentaire' ]
        
  

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['nom', 'prenom', 'email', 'message']