from django.db import models
from django.urls import reverse
#from catalogue.models import Bien,Service
from catalogue.models import SousCategorie


# Create your models here.
class ReferenceCounter(models.Model):
    model_name = models.CharField(max_length=255, unique=True)  # Par exemple: 'categorie', 'famille', etc
    counter = models.PositiveIntegerField(default=0)

    @classmethod
    def get_next_reference(cls, model_name: str, prefix: str, length: int) -> str:
        # Retourne la prochaine référence incrémentée avec un préfixe et une longueur personnalisée.

        ref_counter, created = cls.objects.get_or_create(model_name=model_name)
        ref_counter.counter += 1
        ref_counter.save()
        # Format de la référence avec préfixe et un nombre fixe de chiffres
        return f"{prefix}{ref_counter.counter:0{length}d}"

"""
class Fournisseur(models.Model):
    CHOIX_STATUT = [
        ('Actif', 'Actif'),
        ('Suspendu', 'Suspendu'),
        ('Inactif', 'Inactif'),
    ]
    SPECIALITE_FOURNISSEUR = [
        ('', 'Sélectionner un type'),
        ('Bien', 'Biens'),
        ('Service', 'Services'),

    ]

    reference = models.CharField(max_length=10, blank=True, editable=False)
    nom = models.CharField(max_length=100)
    mail = models.EmailField(max_length=254, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    statut= models.CharField(max_length=10, choices=CHOIX_STATUT, default='Actif')
    specialite= models.CharField(max_length=10, choices=SPECIALITE_FOURNISSEUR, default='draft')
    biens = models.ManyToManyField(Bien, related_name='fournisseurs',blank=True)
    services = models.ManyToManyField(Service, related_name='fournisseurs',blank=True)

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.reference:
            # Utilisation du compteur pour générer la référence
            self.reference = ReferenceCounter.get_next_reference('Fournisseur', 'FOUR-', 3)
        super().save(*args, **kwargs)
"""
class Type(models.Model):
    TYPE = [
        ('', 'Sélectionner un type'),
        ('Bien', 'Biens'),
        ('Service', 'Services'),

    ]
    nom = models.CharField(max_length=10, choices=TYPE, blank=True)

    def __str__(self):
        return self.nom
    
class Fournisseur(models.Model):
    CHOIX_STATUT = [
        ('Actif', 'Actif'),
        ('Suspendu', 'Suspendu'),
        ('Inactif', 'Inactif'),
    ]

    reference = models.CharField(max_length=10, blank=True, editable=False)
    nom = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True, null=True,unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True,unique=True)
    adresse = models.CharField(max_length=100, blank=True, null=True,)
    statut= models.CharField(max_length=10, choices=CHOIX_STATUT, default='Actif')
    types = models.ManyToManyField(Type)
    specialite = models.ManyToManyField(SousCategorie, related_name='fournisseurs',blank=True)

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.reference:
            # Utilisation du compteur pour générer la référence
            self.reference = ReferenceCounter.get_next_reference('Fournisseur', 'FOUR-', 3)
        super().save(*args, **kwargs)

    def get_delete_url(self):
        """Retourne l'URL de suppression pour ce fournisseur"""
        return reverse("Fournisseur:delete", args=[self.pk])

    def get_target_id(self):
        """Retourne l'ID CSS de la ligne du tableau pour HTMX"""
        return f"#fournisseur-{self.pk}"



