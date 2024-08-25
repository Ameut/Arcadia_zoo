from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from pymongo import MongoClient
import logging

from .models import Avis, Animal, Habitat, Image, Race, Service, RapportVeterinaire, NourritureInfo, Contact
from .forms import AvisForm, ContactForm

logger = logging.getLogger(__name__)

# Connexion à la base de données MongoDB Atlas
mongo_client = MongoClient("mongodb+srv://ameur:Ameur81@cluster0.tbfykl4.mongodb.net/")
db = mongo_client['clic-animal']
clicks_collection = db['clicks']

'''urlpatterns = [ 
               
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''

def index(request):  # Vue pour la page d'accueil
    avis_liste = Avis.objects.filter(isVisible=True)
    return render(request, 'liste/index.html', {'avis_liste': avis_liste})

def habitat(request):
    habitats = Habitat.objects.prefetch_related('animaux', 'images').all()  # Préchargez les animaux et les images associées
    context = {'habitats': habitats}
    return render(request, 'liste/habitat.html', context)

def service(request):  # Vue pour la page des services
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'liste/service.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Votre message a été envoyé avec succès, à bientôt !'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = ContactForm()
    return render(request, 'liste/contact.html', {'form': form})

@login_required
def rapport(request):
    rapports = RapportVeterinaire.objects.all().prefetch_related('animal__nourriture_infos')
    nourritures = NourritureInfo.objects.all()
    return render(request, 'liste/rapport.html', {'rapports': rapports, 'nourritures': nourritures})

# Les avis clients

def avis(request):
    avis_liste = Avis.objects.filter(isVisible=True)  # Affiche seulement les avis approuvés
    return render(request, 'liste/avis.html', {'avis': avis_liste})

def avis_page(request):
    if request.method == 'POST':  # Si la requête est de type POST, on crée un formulaire avec les données de la requête
        form = AvisForm(request.POST)
        if form.is_valid():
            avis = form.save(commit=False)
            avis.pseudo = request.user.username
            avis.commentaire = form.cleaned_data['commentaire']
            avis.save()
            return redirect('avis_page')
    else:  # Si la requête n'est pas de type POST, on crée un formulaire vide
        form = AvisForm()
    avis_valides = Avis.objects.filter(isVisible=True)
    return render(request, 'liste/avis.html', {'form': form, 'avis_valides': avis_valides})

def submit_avis(request):  # Vue pour soumettre un avis
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            avis = form.save(commit=False)
            avis.isVisible = False  # L'avis n'est pas visible par défaut
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

@user_passes_test(est_admin)  # Pour vérifier si l'utilisateur est un administrateur
def valider_avis(request, avis_id):
    avis = get_object_or_404(Avis, id=avis_id)
    avis.isVisible = True
    avis.save()
    return redirect('avis')

def avis_visible(request):
    avis_liste = Avis.objects.filter(isVisible=True)  # Récupère uniquement les avis visibles
    return render(request, 'liste/avis_visibles.html', {'avis_liste': avis_liste})

def sync_clicks(request):  # Vue pour synchroniser les clics avec la base de données MongoDB
    clicks = clicks_collection.find()
    for click in clicks:
        animal_id = click['animal_id']
        count = click['count']
        try:
            animal = Animal.objects.get(id=animal_id)  # Récupère l'animal correspondant à l'ID
            animal.clics = count
            animal.save()
        except ObjectDoesNotExist:
            logger.warning(f"Animal with ID {animal_id} does not exist.")
    return redirect(reverse('admin:liste_animal_changelist'))

@csrf_exempt  # Décorateur pour désactiver la protection CSRF
def increment_click(request: HttpRequest, animal_id: int) -> JsonResponse:
    collection = db['clicks']
    collection.update_one(
        {'animal_id': animal_id},
        {'$inc': {'count': 1}},
        upsert=True
    )
    updated_click = collection.find_one({'animal_id': animal_id})
    try:  # Récupère l'animal correspondant à l'ID
        animal = Animal.objects.get(id=animal_id)
        animal.clics = updated_click['count']
        animal.save()
    except ObjectDoesNotExist:
        logger.warning(f"Animal with ID {animal_id} does not exist.")
    return JsonResponse({'new_click_count': updated_click['count']})

def animaux(request):  # Vue pour la liste des animaux
    try:  # Récupère tous les animaux, habitats, images, etc.
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
        return render(request, 'liste/animaux.html', context)  # Retourne la liste des animaux
    except Exception as e:
        logger.error(f"Erreur de la base de données: {str(e)}")
        return HttpResponse("Erreur de la base de données: " + str(e), status=500)

def reset_click(request, animal_id):  # Vue pour remettre à zéro le compteur de clics
    animal = get_object_or_404(Animal, id=animal_id)
    animal.clics = 0
    animal.save()
    return JsonResponse({'message': 'Compteur remis à zéro', 'animal_id': animal_id, 'clics': animal.clics})
