from django.contrib import admin
from django import forms
from .models import Avis, Contact, Utilisateur, Animal, Habitat, Service, Race, RapportVeterinaire, Role, Image,NourritureInfo

# Admin classes
@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ['pseudo', 'commentaire', 'isVisible']
    list_filter = ['isVisible']
    search_fields = ['pseudo', 'commentaire']

# Other admin classes should follow the same pattern as AvisAdmin
# ...

# Form classes
class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['pseudo', 'commentaire', 'isVisible']

# autre class#
admin.site.register(Contact)
admin.site.register(Utilisateur)
admin.site.register(Animal)
admin.site.register(Habitat)
admin.site.register(Service)
admin.site.register(Race)
admin.site.register(RapportVeterinaire)
admin.site.register(Role)
admin.site.register(Image)
admin.site.register(NourritureInfo)