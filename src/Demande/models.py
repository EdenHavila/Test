from django.db import models
from datetime import date
from django.urls import reverse
from django.conf import settings

from catalogue.models import  Bien,Service
from django.utils import timezone

"""
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
"""



"""
class Demande(models.Model):
    CHOIX_DEMANDE = [
        ('', 'Selectionnez un type'),
        ('Bien', 'Bien'),
        ('Service', 'Service'),
    ]
    reference = models.CharField(max_length=10, blank=True, editable=False)
    date = models.DateField(default=date.today)
    type_demande = models.CharField(max_length=10, choices=CHOIX_DEMANDE,default='draft')
    fichier_joint = models.FileField(upload_to='Demande/fichiers/', null=True, blank=True)
    services = models.ManyToManyField(Service,through='DetailsDemande',blank=True)
    biens = models.ManyToManyField(Bien, through='DetailsDemande',blank=True)


    def __str__(self):
        return f"Demande_{self.reference}"

    def save(self, *args, **kwargs):
        if not self.reference:
            # Utilisation du compteur pour générer la référence
            self.reference = ReferenceCounter.get_next_reference('Demande', 'DEM', 6)
        super().save(*args, **kwargs)

"""



class Demande(models.Model):
    TYPE_CHOICES = [
        ("Demandeur", "Demandeur"),
        ("Gestionnaire", "Gestionnaire"),
    ]
    NATURE_DEMANDE = [
        ('', 'Selectionnez un type'),
        ('Bien', 'Bien'),
        ('Service', 'Service'),
    ]
    STATUT_DEMANDE = [
        ('', 'Selectionnez un type'),
        ('En cours', 'En cours'),
        ('Validée', 'Validée'),
        ('Rejetée', 'Rejetée'),
        ('Traitement', 'Traitement'),
        ('Traitée', 'Traitée'),
    ]

    code_demande = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='demandes',
        null=True,
        blank=True
    )
    type_demande = models.CharField(max_length=20, choices=TYPE_CHOICES)
    nature_demande = models.CharField(max_length=10,choices=NATURE_DEMANDE)
    date_demande = models.DateField(default=date.today)
    fichier_joint = models.FileField(upload_to='Demande/fichiers/', null=True, blank=True)
    date_enregistrement = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")
    date_mise_a_jour = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    motif_demande = models.TextField()
    statut_demande = models.CharField(max_length=50, choices=STATUT_DEMANDE, default='En cours')

    # Nouveau champ : visible uniquement si type_demande = Gestionnaire
    # Auto-association récursive :
    demandes_associees = models.ManyToManyField(
        'self',  # auto-association
        symmetrical=False,  # A regroupe B ≠ B regroupe A
        related_name='regroupee_par',  # permet de savoir par qui une demande est regroupée
        blank=True
    )


    def save(self, *args, **kwargs):
        if not self.code_demande:
            self.code_demande = self.generate_code()
        super().save(*args, **kwargs)


    def generate_code(self):
        now = timezone.now()
        year = now.year
        month = f"{now.month:02d}"

        # 1️⃣ Définir le code du type de demande
        type_code = "DEM" if self.type_demande == "Demandeur" else "GES"

        # 2️⃣ Compter les demandes avec même type + même mois + même année
        count = Demande.objects.filter(
            type_demande=self.type_demande,
            date_demande__year=year,
            date_demande__month=now.month
        ).count() + 1

        compteur = f"{count:03d}"

        # 3️⃣ Générer le code final
        return f"DEM-{type_code}-{year}-{month}-{compteur}"

    def __str__(self):
        return self.code_demande

    def get_delete_url(self):
        """Retourne l'URL de suppression pour cette demande"""
        return reverse("Demande:supprimer-demande", args=[self.pk])

    def get_target_id(self):
        """Retourne l'ID CSS de la ligne du tableau pour HTMX"""
        return f"#demande-{self.pk}"


class DetailsDemande(models.Model):
    CHOIX_TYPE = [
        ('', 'Selectionnez un type'),
        ('Bien', 'Bien'),
        ('Service', 'Service'),
    ]
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CHOIX_TYPE,default='draft')
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    quantite = models.PositiveIntegerField()
    #motif = models.TextField( blank=True)


    def __str__(self):
        return f"{self.demande.reference} — {self.bien.designation} "

