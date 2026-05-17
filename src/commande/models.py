from datetime import date
from django.db import models
from django.urls import reverse
from Demande.models import Demande
from Fournisseur.models import Fournisseur
from catalogue.models import Bien, Service
from monprojet.utils.code_generator import generate_monthly_code

# Create your models here.

class Commande(models.Model):
    STATUT_CHOICES = (
        ('en_cours', 'En Cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    )
    code_cmnd = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    date_cmnd =models.DateField(default=date.today)
    statut_cmnd = models.CharField(max_length=20, choices=STATUT_CHOICES)
    fichier_bon_cmnd = models.FileField(upload_to='Commandes/', null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)  # utile pour l'historique

    def save(self, *args, **kwargs):
        if not self.code_cmnd:
            self.code_cmnd = generate_monthly_code(
                prefix="CMND",
                model_class=Commande,
                date_field="date_cmnd" # champ date à utiliser
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_cmnd

    # Méthodes helper pour les templates
    def get_delete_url(self):
        return reverse("commande:supprimer-commande", args=[self.id])
    
    def get_target_id(self):
        return f"#commande-{self.id}"
    
    @property
    def montant_total(self):
        """Calcule le montant total de toutes les lignes de la commande"""
        total = sum(
            ligne.total or 0 
            for ligne in self.lignes.all() 
            if ligne.total is not None
        )
        return total if total > 0 else None
    
    @property
    def nombre_lignes(self):
        """Retourne le nombre de lignes de commande"""
        return self.lignes.count()
    




class LigneCommande(models.Model):
    TYPE_CHOICES = (
        ('', 'Sélectionner un type'),
        ('Bien', 'Bien'),
        ('Service', 'Service'),
    )

    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    bien = models.ForeignKey(Bien, null=True, blank=True, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.prix_unitaire and self.quantite:
            self.total = self.prix_unitaire * self.quantite
        super().save(*args, **kwargs)

    def __str__(self):
        if self.bien:
            return f"{self.bien.designation} x {self.quantite}"
        elif self.service:
            return f"{self.service.designation} x {self.quantite}"
        return f"Ligne {self.pk}"


class Livraison(models.Model):
    """Modèle pour gérer les livraisons liées aux commandes"""
    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('partielle', 'Partielle'),
        ('complete', 'Complète'),
        ('annulee', 'Annulée'),
    )
    
    code_livraison = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='livraisons')
    date_livraison = models.DateField(default=date.today)
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    fichier_bon_livraison = models.FileField(upload_to='Livraisons/', null=True, blank=True)
    observation = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code_livraison:
            self.code_livraison = generate_monthly_code(
                prefix="LIV",
                model_class=Livraison,
                date_field="date_livraison"
            )
        super().save(*args, **kwargs)
        if self.statut == 'complete' and self.commande_id:
            Commande.objects.filter(pk=self.commande_id).update(statut_cmnd='terminee')

    def __str__(self):
        return self.code_livraison

    def get_delete_url(self):
        return reverse("commande:supprimer-livraison", args=[self.id])
    
    def get_target_id(self):
        return f"#livraison-{self.id}"
    
    class Meta:
        ordering = ['-date_enregistrement']
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"