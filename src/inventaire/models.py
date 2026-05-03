from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils import timezone
from catalogue.models import Bien
from accounts.models import User
from monprojet.utils.code_generator import generate_code

# Modèle Stock
class Stock(models.Model):
    # Unités possibles
    UNITE_CHOICES = [
        ('', '- Choisir une unité -'),
        ('piece', 'Pièce'),
        ('boite', 'Boîte'),
        ('litre', 'Litre'),
        ('autre', 'Autre'),
    ]

    # Statuts possibles
    STATUT_CHOICES = [
        ('', '- Choisir un statut -'),
        ('disponible', 'Disponible'),
        ('indisponible', 'Indisponible'),
    ]

    # Lieux de stockage possibles (pour le champ choices)
    LIEU_CHOICES = [
        ('', '- Choisir un lieu -'),
        ('entrepot1', 'Entrepôt 1'),
        ('entrepot2', 'Entrepôt 2'),
        ('stock_central', 'Stock central'),
        ('autre', 'Autre'),
    ]

    # Mapping des lieux vers codes courts (pour la génération du code)
    LIEU_CODE_MAP = {
        'entrepot1': 'E1',
        'entrepot2': 'E2',
        'stock_central': 'SC',
        'autre': 'AU',
    }

    # Champs du modèle
    code = models.CharField("Code", max_length=20, unique=True, blank=True)
    quantite_disponible = models.PositiveIntegerField("Quantité disponible", default=1)
    lieu_stockage = models.CharField("Lieu de stockage", max_length=100, choices=LIEU_CHOICES)
    responsable_stock = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Responsable du stock", related_name='stocks_responsable',limit_choices_to={'role__nom_role': 'gestionnaire'})
    date_mise_a_jour = models.DateTimeField("Date de mise à jour", default=timezone.now, blank=True, null=True)
    statut_bien = models.CharField("Statut du bien", max_length=20, choices=STATUT_CHOICES, blank=True, null=True,default='disponible')
    unite = models.CharField("Unité", max_length=10, choices=UNITE_CHOICES, default='piece')
    niveau_alerte = models.PositiveIntegerField("Seuil d'alerte", default=1)
    
    # Relation avec Bien
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, related_name='stocks')

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ['lieu_stockage', 'bien']
        # Contrainte : un bien ne peut avoir qu'un seul stock par lieu
        unique_together = ['bien', 'lieu_stockage']

    def __str__(self):
        return f"{self.code} - {self.bien.designation}"
    
    def save(self, *args, **kwargs):
        if not self.code:
            # Récupérer le code court du lieu (E1, E2, SC, AU)
            lieu_code = self.LIEU_CODE_MAP.get(self.lieu_stockage, 'XX')
            
            # Compter les stocks existants pour ce lieu
            count = Stock.objects.filter(lieu_stockage=self.lieu_stockage).count() + 1
            
            # Générer le code : STK-E1-001
            self.code = f"STK-{lieu_code}-{count:03d}"
        super().save(*args, **kwargs)

    @property
    def alerte_stock(self):
        """Retourne True si le stock est inférieur au seuil d'alerte."""
        return self.quantite_disponible <= self.niveau_alerte

    def get_delete_url(self):
        """Retourne l'URL de suppression pour ce stock"""
        return reverse("inventaire:delete-stock", args=[self.pk])

    def get_target_id(self):
        """Retourne l'ID CSS de la ligne du tableau pour HTMX"""
        return f"#stock-{self.pk}"





class MouvementLogistique(models.Model):
    # Types de mouvement
    TYPE_CHOICES = [
        ('ENT', 'Entrée'),
        ('SOR', 'Sortie'),
        ('TRF', 'Transfert'),
        ('RET', 'Retour'),
        ('COR', 'Correction'),
    ]

    # Sources possibles
    SOURCE_CHOICES = [
        ('entrepot', 'Entrepôt'),
        ('fournisseur', 'Fournisseur'),
        ('stock_central', 'Stock central'),
        ('autre', 'Autre'),
    ]

    # Types de destination
    DEST_TYPE_CHOICES = [
        ('employe', 'Employé'),
        ('service', 'Service'),
        ('stock', 'Stock'),
        ('autre', 'Autre'),
    ]

    # Champs principaux
    code = models.CharField("Code unique", max_length=20, unique=True, blank=True)
    date_mouvement = models.DateTimeField(default=timezone.now)
    type_mouvement = models.CharField("Type de mouvement", max_length=20, choices=TYPE_CHOICES)
    quantite = models.PositiveIntegerField("Quantité")
    source = models.CharField("Source", max_length=50, choices=SOURCE_CHOICES)
    destination_type = models.CharField("Type de destination", max_length=20, choices=DEST_TYPE_CHOICES)
    destination = models.CharField("Destination", max_length=100, blank=True, null=True)
    justification = models.TextField("Justification / Motif", blank=True, null=True)
    reference_document = models.FileField("Référence documentaire", upload_to='documents/', blank=True, null=True)

    # Relations
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mouvements')
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='mouvements', verbose_name="Stock concerné")
    #bien = models.ForeignKey(Bien, on_delete=models.CASCADE, related_name='mouvements')


    class Meta:
        verbose_name = "Mouvement logistique"
        verbose_name_plural = "Mouvements logistiques"
        ordering = ['-date_mouvement']

    def __str__(self):
        return f"{self.code}"
    
    def clean(self):
        """Validation pour que la quantité soit > 0"""
        if self.quantite <= 0:
            from django.core.exceptions import ValidationError
            raise ValidationError({'quantite': "La quantité doit être supérieure à 0."})

    def get_delete_url(self):
        """Retourne l'URL de suppression pour ce mouvement"""
        return reverse("inventaire:delete-mouvement", args=[self.pk])

    def get_target_id(self):
        """Retourne l'ID CSS de la ligne du tableau pour HTMX"""
        return f"#mouvement-{self.pk}"
        
    
    def save(self, *args, **kwargs):
        if not self.code:  # Génère le code seulement si il n'existe pas
            self.code = generate_code(
                prefix="MVT", 
                type_code=self.type_mouvement, 
                model_class=MouvementLogistique,
                type_field_name="type_mouvement",
                date_field="date_mouvement"
            )
        super().save(*args, **kwargs)    