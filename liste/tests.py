from django.test import TestCase
from django.urls import reverse
from .models import Animal, Habitat, Race, RapportVeterinaire, NourritureInfo
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User


class HabitatViewTests(TestCase):

    def setUp(self):
        # Créer un habitat
        self.habitat = Habitat.objects.create(nom="Savane", description="Habitat pour les animaux de savane")
        
        # Créer une race d'animal
        self.race = Race.objects.create(label="Lion")
        
        # Créer un fichier image 
        image = SimpleUploadedFile("lion.jpg", b"file_content", content_type="image/jpeg")
        
        # Créer un animal associé à cet habitat avec une image
        self.animal = Animal.objects.create(
            prenom="Simba",
            etat="En bonne santé",
            habitat=self.habitat,
            race=self.race,
            image=image,
            clics=5
        )

    def test_habitat_view_displays_animals(self):
        # Accéder à la vue 'habitat'
        response = self.client.get(reverse('habitat'))
        
        # Vérifier que la page s'affiche correctement
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que le nom de l'habitat est dans la réponse
        self.assertContains(response, "Savane")
        
        # Vérifier que les informations sur l'animal sont dans la réponse
        self.assertContains(response, "Simba")
        self.assertContains(response, "Lion")


from django.test import TestCase
from django.urls import reverse
from .models import Contact
from .forms import ContactForm

class ContactViewTests(TestCase):

    def test_contact_page_displays_correctly(self):
        # Accéder à la vue 'contact'
        response = self.client.get(reverse('contact'))
        
        # Vérifier que la page s'affiche correctement
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contactez-nous")
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_form_submission(self):
        # Données pour le formulaire de contact
        form_data = {
            'nom': 'Test',
            'prenom': 'User',
            'email': 'testuser@example.com',
            'message': 'Ceci est un message de test.'
        }

        # Soumettre le formulaire via un POST
        response = self.client.post(reverse('contact'), data=form_data)

        # Vérifier que la redirection a bien eu lieu après la soumission
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

        # Vérifier que le contact a bien été créé dans la base de données
        self.assertTrue(Contact.objects.filter(email='testuser@example.com').exists())
class RapportViewTests(TestCase):

    def setUp(self):
        # Créer un utilisateur et se connecter
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        
        # Créer un habitat
        self.habitat = Habitat.objects.create(nom="Savane", description="Habitat pour les animaux de savane")
        
        # Créer une race
        self.race = Race.objects.create(label="Lion")
        
        # Créer un animal associé à cet habitat et cette race
        self.animal = Animal.objects.create(
            prenom="Simba",
            etat="En bonne santé",
            habitat=self.habitat,
            race=self.race,
            clics=5
        )
        
        # Créer un rapport vétérinaire pour cet animal
        self.rapport = RapportVeterinaire.objects.create(
            date="2024-08-13",
            detail="Vaccination annuelle et examen général.",
            animal=self.animal
        )
        
        # Créer une information alimentaire pour cet animal
        self.nourriture = NourritureInfo.objects.create(
            animal=self.animal,
            nourriture_proposee="Viande de boeuf",
            grammage_nourriture=5.0,
            date_consommation="2024-08-12",
            heure_consommation="12:30:00"
        )

def test_rapport_page_displays_correctly(self):
    # Accéder à la vue 'rapport'
    response = self.client.get(reverse('rapport'))

    # Imprimer le contenu de la réponse pour débogage (optionnel)
    print(response.content.decode())  # À utiliser si vous voulez voir le contenu complet de la réponse

    # Vérifier que la page s'affiche correctement
    self.assertEqual(response.status_code, 200)

    # Vérifier que le rapport vétérinaire est affiché (sans vérifier la date)
    self.assertContains(response, "Vaccination annuelle et examen général.")
    
    # Vérifier que les informations alimentaires sont affichées
    self.assertContains(response, "Viande de boeuf")
    self.assertContains(response, "5.0")
    self.assertContains(response, "2024-08-12")
    self.assertContains(response, "12:30:00")
    
    from django.test import TestCase
from .models import Avis

class AvisModelTest(TestCase):

    def setUp(self):
        # Configuration initiale avant chaque test
        self.avis = Avis.objects.create(
            pseudo="TestUser",
            commentaire="Ceci est un test de commentaire.",
            isVisible=False
        )

    def test_avis_creation(self):
        # Test de la création d'un avis
        avis = Avis.objects.get(pseudo="TestUser")
        self.assertEqual(avis.commentaire, "Ceci est un test de commentaire.")
        self.assertFalse(avis.isVisible)


    def test_avis_visibility_toggle(self):
        # Test pour vérifier la modification de la visibilité de l'avis
        avis = Avis.objects.get(pseudo="TestUser")
        avis.isVisible = True
        avis.save()
        self.assertTrue(avis.isVisible)

    def test_avis_str_method(self):
        # Test pour vérifier la méthode __str__ du modèle
        avis = Avis.objects.get(pseudo="TestUser")
        self.assertEqual(str(avis), "TestUser: Ceci est un test de ...")

from django.core.exceptions import ValidationError

def test_invalid_avis(self):
    # Test de la création d'un avis avec des données invalides
    avis = Avis(pseudo="", commentaire="", isVisible=True)
    with self.assertRaises(ValidationError):
        avis.full_clean()  # Appelle la validation des champs
        avis.save()  # Sauvegarde l'instance d'Avis

