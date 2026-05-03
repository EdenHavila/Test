# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

#on_delete=models.SET_NULL :si le rôle est supprimé, l’utilisateur garde un rôle null.
#null=True, blank=True : permet de créer des utilisateurs avant d’assigner un rôle si besoin.
class Role(models.Model):
    ROLE_CHOICES = [
        ('demandeur', 'Demandeur'),
        ('gestionnaire', 'Gestionnaire'),
        ('admin', 'Admin'),
    ]

    nom_role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='demandeur', unique=True)

    def __str__(self):
        return self.nom_role


class User(AbstractUser):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
    ]
    USERNAME_FIELD = 'username'  # champ principal pour l'authentification
    REQUIRED_FIELDS = ['first_name', 'last_name','email']
    email = models.EmailField(unique=True)
    statut_utilisateur = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='actif'
    )

    date_creation_utilisateur = models.DateTimeField(default=timezone.now)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.username} ({self.email})"
# Dans settings.py, définir :
# AUTH_USER_MODEL = "accounts.User"

