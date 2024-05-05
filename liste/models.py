from django.db import models
from django.utils import timezone
timezone.now()
from datetime import datetime, timedelta



from django.utils.translation import gettext_lazy as _

class Role(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label

class Utilisateur(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    # Chaque utilisateur possède un rôle
    role = models.ForeignKey(Role, related_name='utilisateurs', on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class Service(models.Model):
    nom = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    roles = models.ManyToManyField('Role', related_name='services')
    heure_ouverture = models.TimeField(verbose_name="Heure d'ouverture", null=True, blank=True)
    heure_fermeture = models.TimeField(verbose_name="Heure de fermeture", null=True, blank=True)

    def __str__(self):
        return self.nom

class Habitat(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()
    commentaire_habitat = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nom

class Race(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label

class Animal(models.Model):
    prenom = models.CharField(max_length=50)
    etat = models.CharField(max_length=50)
    habitat = models.ForeignKey(Habitat, related_name='animaux', on_delete=models.CASCADE)
    race = models.ForeignKey(Race, related_name='animaux', on_delete=models.SET_NULL, null=True, default=1)
    image = models.ImageField(upload_to='animals/', verbose_name=_("Image de l'animal"))
    clics = models.IntegerField(default=0)  # Champ pour les cliques sur l'animal

    def __str__(self):
        return f"{self.prenom} - {self.race}"

class RapportVeterinaire(models.Model):
    date = models.DateField()
    detail = models.TextField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='rapports_veterinaires')

    def __str__(self):
        return f"{self.date} - {self.animal}"


class NourritureInfo(models.Model):
    rapport = models.ForeignKey(RapportVeterinaire, on_delete=models.CASCADE, related_name='nourriture_infos')
    nourriture_proposee = models.CharField(max_length=255, verbose_name=_("Nourriture proposée"))
    grammage_nourriture = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name=_("Grammage de la nourriture"))
    # Utilisez `auto_now_add=True` pour la date de consommation pour enregistrer la date de création de l'objet
    date_consommation = models.DateField(verbose_name=_("Date de consommation"), default=timezone.now)  # use timezone.now without ()
    heure_consommation = models.TimeField(verbose_name=_("Heure de consommation"), default=timezone.now)  # same here

    def __str__(self):
        return f"Nourriture: {self.nourriture_proposee}, Grammage: {self.grammage_nourriture} ({self.date_consommation} à {self.heure_consommation})"

class Image(models.Model):
    image_data = models.ImageField(upload_to='images/')
    # Une image est associée à un animal
    animal = models.ForeignKey('Animal', related_name='images', on_delete=models.CASCADE)
    # Ajout d'une clé étrangère faisant référence à Habitat
    habitat = models.ForeignKey('Habitat', related_name='images', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.animal} - {self.habitat}"

class Avis(models.Model):
    pseudo = models.CharField(max_length=50)
    commentaire = models.TextField()
    isVisible = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.pseudo}: {self.commentaire[:20]}..."
    
   
class Contact(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True) 
    message = models.TextField()

    def __str__(self):
        return self.nom


