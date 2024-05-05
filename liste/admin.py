from django.contrib import admin
from django import forms
from pymongo import MongoClient
from django.contrib import messages

from .models import Avis, Contact, Utilisateur, Animal, Habitat, Service, Race, RapportVeterinaire, Role, Image,NourritureInfo

# Admin classes
@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ['pseudo', 'commentaire', 'isVisible']
    list_filter = ['isVisible']
    search_fields = ['pseudo', 'commentaire']
    
mongo_client = MongoClient('localhost', 27017)
db = mongo_client['clic-animal']
clicks_collection = db['clicks']

# Définir la fonction reset_clicks
# pour mettre les compteur a 0 cocher la case puis aller dans le menu deroulant et cliquer sur reset clicks
def reset_clicks(modeladmin, request, queryset):
    # Réinitialiser MongoDB
    clicks_collection.update_many({}, {'$set': {'count': 0}})
    # Réinitialiser Django
    queryset.update(clics=0)
    modeladmin.message_user(request, "Les compteurs de clics ont été réinitialisés.")

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'etat', 'habitat', 'race', 'clics')
    actions = [reset_clicks]
# ...

# Form classes
class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['pseudo', 'commentaire', 'isVisible']

# autre class#
admin.site.register(Contact)
admin.site.register(Utilisateur)

admin.site.register(Habitat)
admin.site.register(Service)
admin.site.register(Race)
admin.site.register(RapportVeterinaire)
admin.site.register(Role)
admin.site.register(Image)
admin.site.register(NourritureInfo)
admin.site.register(Animal, AnimalAdmin)
