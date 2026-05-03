from django.db import models
from django.forms import forms


# Create your models here.

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    # Champ pour une sélection de choix (ex : statut de l'article)
    STATUS_CHOICES = [
        ('', 'choisissez'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.titre


class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.nom