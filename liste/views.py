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

def animaux(request):
    try:
        client = MongoClient('localhost', 27017)# MongoClient('localhost', 27017)
        db = client['clic-animal']
        clicks_collection = db['clicks']

        animals = Animal.objects.all()
        habitats = Habitat.objects.all()
        images = Image.objects.all()
        races = Race.objects.all()

        for animal in animals:#  pour chaque animal, obtenir le nombre de clics associés
            clicks_data = clicks_collection.find_one({'animal_id': animal.id})
            animal.clicks = clicks_data['count'] if clicks_data else 0

        context = {
            'animals': animals,
            'habitats': habitats,
            'images': images,
            'races': races
        }

        return render(request, 'liste/animaux.html', context)   # Renvoyer la réponse HTTP avec les informations des animaux et les images
    except Exception as e:#  en cas d'erreur lors de l'accès à la base de données
        return HttpResponse("Erreur de la base de donée: " + str(e), status=500)

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

# Logger pour enregistrer les messages d'erreur
# tester si l'utilisateur est un vétérinaire pour accéder à la page de rapport
logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                if user.groups.filter(name='vétérinaire').exists():
                    login(request, user)
                    return redirect('rapport')
                else:
                    logger.info(f"Access denied for user {username}: not a member of 'vétérinaire' group")
                    messages.error(request, "Accès refusé. Vous devez être membre du groupe 'vétérinaire'.")
                    return redirect('login1')
            else:
                logger.warning(f"Invalid login attempt for username: {username}")
                messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
        else:
            logger.error("Form submission invalid")
            messages.error(request, "Soumission de formulaire invalide.")
    else:
        form = AuthenticationForm()
    return render(request, 'liste/login1.html', {'form': form})

def user_is_veterinaire(user):
    in_group = user.groups.filter(name='vétérinaire').exists()
    logger.info(f"User {user.username} in 'vétérinaire': {in_group}")
    return in_group

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

def get_db_handle():
    client = MongoClient(host='localhost', port=27017)  # Mettez à jour avec les paramètres MongoDB
    return client['clic-animal']

def increment_click(request, animal_id):
    print(f"Incrementing click for animal ID: {animal_id}")   
    db = get_db_handle()
    collection = db.clicks
    result = collection.update_one({'animal_id': animal_id}, {'$inc': {'count': 1}}, upsert=True)
    print(f"MongoDB update result: {result.matched_count}")
    return redirect('animaux')


    
    
    '''animals = Animal.objects.all().prefetch_related('images')
    animal_info = []
    for animal in animals:
        # Pour chaque animal, obtenir toutes les images associées
        images_html = ''.join([f'<img src="{image.image_data.url}" alt="{animal.prenom}" style="width:100px;height:auto;">' for image in animal.images.all()])
        # Construire la chaîne de caractères incluant les balises <img> pour les images
        animal_str = f"{animal.prenom} - Race: {animal.race}, Habitat: {animal.habitat}, Images: {images_html}"
        animal_info.append(animal_str)
    
    animal_info_str = "<br>".join(animal_info)  # Utiliser <br> pour le retour à la ligne
    # Renvoyer la réponse HTTP avec les informations des animaux et les images
    return HttpResponse(f'Mes animaux :<br>{animal_info_str}')'''
