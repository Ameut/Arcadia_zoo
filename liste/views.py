from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from .models import Avis
from .forms import AvisForm
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from . import views
from django.contrib.auth import logout, login
from django.contrib import messages
import logging


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from .forms import ContactForm
from pymongo import MongoClient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




from .models import Animal,Habitat,Image,Race,Service,Role,Utilisateur,RapportVeterinaire,Avis,Contact,NourritureInfo




'''urlpatterns = [ 
               
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''

def index(request):
    avis_liste = Avis.objects.filter(isVisible=True)
    return render(request, 'liste/index.html', {'avis_liste': avis_liste})
def habitat(request):
    habitats = Habitat.objects.prefetch_related('animaux', 'images').all()# Préchargez les animaux et les images associées
    context = {'habitats': habitats}
    return render(request, 'liste/habitat.html', context)


def service(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'liste/service.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Ajoutez ici la logique pour rediriger l'utilisateur après la soumission du formulaire
            return redirect('index')  # retour a la page d'acceuil
    else:
        form = ContactForm()

    return render(request, 'liste/contact.html', {'form': form})
#  rapport veto    #



#@user_passes_test(user_is_veterinaire)
@login_required
def rapport(request):
     rapports = RapportVeterinaire.objects.all().prefetch_related('nourriture_infos')
    
     return render(request, 'liste/rapport.html', {'rapports': rapports})
    
# les avis clients
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden



def avis(request):
    # Récupération de tous les avis visibles
    avis_liste = Avis.objects.filter(isVisible=True)  # Affiche seulement les avis approuvés
    return render(request, 'liste/avis.html', {'avis': avis_liste})

def avis_page(request):
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            avis = form.save(commit=False)
            avis.pseudo = request.user.username
            avis.commentaire = form.cleaned_data['commentaire']
            avis.save()
            return redirect('avis_page')
    else:
        form = AvisForm()
    avis_valides = Avis.objects.filter(isVisible=True)
    return render(request, 'liste/avis.html', {'form': form, 'avis_valides': avis_valides})


def submit_avis(request):
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            # Ici, form.save(commit=False) crée une instance d'Avis sans sauvegarder en DB
            avis = form.save(commit=False)
            
            # Plus besoin de cette ligne puisque le pseudo est déjà inclus dans le formulaire
            # avis.pseudo = request.user.username
            
            avis.isVisible = False  # Cela peut rester inchangé

            avis.save()  # Sauvegarde l'instance d'Avis en DB avec le pseudo du formulaire
            return redirect('avis_visibles')
    else:
        form = AvisForm()

    return render(request, 'liste/submit_avis.html', {'form': form})
def validation_avis(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    avis_non_valides = Avis.objects.filter(isVisible=False)
    return render(request, 'liste/validation_avis.html', {'avis_non_valides': avis_non_valides})


def est_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(est_admin)
def valider_avis(request, avis_id):
    avis = get_object_or_404(Avis, id=avis_id)
    avis.isVisible = True
    avis.save()
    return redirect('avis')

def avis_visible(request):
    avis_liste = Avis.objects.filter(isVisible=True)  # Récupère uniquement les avis visibles
    return render(request, 'liste/avis_visibles.html', {'avis_liste': avis_liste})

#connection à la base de données mongo


from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

logger = logging.getLogger(__name__)

mongo_client = MongoClient('localhost', 27017)
db = mongo_client['clic-animal']
clicks_collection = db['clicks']

def sync_clicks(request):# Fonction pour synchroniser les clics de MongoDB avec Django
    clicks_collection = db['clicks']
    clicks = clicks_collection.find()

    for click in clicks:
        animal_id = click['animal_id']
        count = click['count']
        try:
            animal = Animal.objects.get(id=animal_id)
            animal.clics = count
            animal.save()
        except ObjectDoesNotExist:
            logger.warning(f"Animal with ID {animal_id} does not exist.")

    return redirect(reverse('admin:liste_animal_changelist'))

@csrf_exempt#  pour autoriser les requêtes POST sans jeton CSRF
def increment_click(request: HttpRequest, animal_id: int) -> JsonResponse:
    collection = db['clicks']
    collection.update_one(
        {'animal_id': animal_id},
        {'$inc': {'count': 1}},
        upsert=True
    )
    updated_click = collection.find_one({'animal_id': animal_id})

    # Mettre à jour le champ clics dans Django
    try:
        animal = Animal.objects.get(id=animal_id)
        animal.clics = updated_click['count']
        animal.save()
    except ObjectDoesNotExist:
        logger.warning(f"Animal with ID {animal_id} does not exist.")

    return JsonResponse({'new_click_count': updated_click['count']})

def animaux(request):
    try:
        clicks_collection = db['clicks']
        animals = Animal.objects.all()
        habitats = Habitat.objects.all()
        images = Image.objects.all()
        races = Race.objects.all()

        for animal in animals:
            clicks_data = clicks_collection.find_one({'animal_id': animal.id})
            animal.clics = clicks_data['count'] if clicks_data else 0

        context = {
            'animals': animals,
            'habitats': habitats,
            'images': images,
            'races': races
        }

        return render(request, 'liste/animaux.html', context)
    except Exception as e:
        logger.error(f"Erreur de la base de données: {str(e)}")
        return HttpResponse("Erreur de la base de données: " + str(e), status=500)

def reset_click(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    animal.clics = 0
    animal.save()
    return JsonResponse({'message': 'Compteur remis à zéro', 'animal_id': animal_id, 'clics': animal.clics})