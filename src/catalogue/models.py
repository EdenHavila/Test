from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import transaction
# Create your models here.
class ReferenceCounter(models.Model):
    model_name = models.CharField(max_length=255, unique=True)# Par exemple: 'categorie', 'famille', etc
    counter = models.PositiveIntegerField(default=0)

    @classmethod
    def get_next_reference(cls, model_name: str, prefix: str, length: int) -> str:
        #Retourne la prochaine référence incrémentée avec un préfixe et une longueur personnalisée.

        ref_counter, created = cls.objects.get_or_create(model_name=model_name)
        ref_counter.counter += 1
        ref_counter.save()
        # Format de la référence avec préfixe et un nombre fixe de chiffres
        return f"{prefix}{ref_counter.counter:0{length}d}"


    """""
    # Champ pour une sélection de choix (ex : statut de l'article)
    STATUS_CHOICES = [
        ('', 'choisissez'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    """""

class Famille(models.Model):
    reference = models.CharField(max_length=10, blank=True, editable=False)
    designation = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if len(self.designation) < 3:
            raise ValueError("Le nom doit contenir au moins 3 caractères.")
        self.reference = self.designation[:3].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.designation


class Categorie(models.Model):
    TYPE = [
        ('', 'Sélectionner un type'),
        ('Bien', 'Biens'),
        ('Service', 'Services'),

    ]

    reference = models.CharField(max_length=10, blank=True, editable=False)
    designation = models.CharField(max_length=200)
    famille = models.ForeignKey(Famille,  on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Crée la référence de la catégorie en combinant la référence de la famille et le nom de la catégorie
        self.reference = f"{self.famille.reference}-{self.designation[:3].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.designation

class SousCategorie(models.Model):
    TYPE = [
        ('', 'Sélectionner un type'),
        ('Bien', 'Biens'),
        ('Service', 'Services'),

    ]                                                           
    reference = models.CharField(max_length=10, blank=True, editable=False)
    type = models.CharField(max_length=10, choices=TYPE,null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='sous_categories')
    nom = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Crée la référence de la sous-catégorie en combinant la référence de la catégorie et le nom de la sous-catégorie
        self.reference = f"{self.categorie.reference}-{self.nom[:3].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nom}'

class Bien(models.Model):
    FREQUENCE_CHOICES = [
        ('', 'choisissez'),
        ('hebdomadaire ', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
        ('annuel', 'Annuel '),
        ('ponctuel','Ponctuel  '),
        ('occasionnel','Occasionnel  '),
        ('quotidien','Quotidien  '),
        ('autre','Autre  '),
    ]
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE, related_name='biens',default=1)
    reference = models.CharField(max_length=10, blank=True, editable=False)
    designation = models.CharField(max_length=200)
    frequence_utilisation = models.CharField(max_length=20, choices=FREQUENCE_CHOICES, default='draft')
    numero = models.PositiveIntegerField(blank=True,null=True)  # Un numéro unique pour chaque bien
    
    # Champs facultatifs
    marque = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marque")
    modele = models.CharField(max_length=100, blank=True, null=True, verbose_name="Modèle")
    informations_complementaires = models.TextField(blank=True, null=True, verbose_name="Informations complémentaires")

    def get_delete_url(self):
        return reverse("catalogue:delete-bien", args=[self.id])
    def get_target_id(self):
        return f"#bien-{self.id}"

    def get_next_numero(self):
        """Récupère le prochain numéro d'identification pour la sous-catégorie."""
        with transaction.atomic(): # Assure que l'opération est atomique pour éviter les conflits de concurrence(évite la collision de numéro lorsque plusieurs biens sont créés simultanément)
            # Recherche du plus grand numéro déjà existant dans la même sous-catégorie
            max_numero = Bien.objects.filter(sous_categorie=self.sous_categorie).aggregate(models.Max('numero'))['numero__max']
            if max_numero is None:
                return 1  # Si aucun bien n'existe encore dans cette sous-catégorie, commence par 1
            return max_numero + 1  # Sinon, incrémente le plus grand numéro trouvé

    def save(self, *args, **kwargs):
        """Sauvegarde l'objet bien avec une référence générée et un numéro unique."""
        if self.numero is None:  # Si le numéro n'est pas défini, l'assigner automatiquement
            self.numero = self.get_next_numero()

        if Bien.objects.filter(numero=self.numero).exists():     # Vérifie si le numéro existe déjà pour cette sous-catégorie (en cas de race condition)
            self.numero = self.get_next_numero()   # Si le numéro existe déjà, réessayer de récupérer un nouveau numéro

        # Générer la référence du bien : combinaison de la référence de la famille, de la catégorie, de la sous-catégorie et du numéro unique du bien
        self.reference = f"{self.sous_categorie.reference}-{str(self.numero).zfill(3)}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.designation


class Service(models.Model):
    FREQUENCE = [
        ('', 'choisissez'),
        ('hebdomadaire ', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
        ('annuel', 'Annuel '),
        ('ponctuel','Ponctuel  '),
    ]
    categorie = models.ForeignKey(Categorie, related_name='services', on_delete=models.CASCADE)
    reference = models.CharField(max_length=10, blank=True, editable=False)
    designation = models.CharField(max_length=200)
    frequence  = models.CharField(max_length=20, choices=FREQUENCE, default='draft')
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.reference:
            # Utilisation du compteur pour générer la référence
            self.reference = ReferenceCounter.get_next_reference('Service', 'SERV',3)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.designation
