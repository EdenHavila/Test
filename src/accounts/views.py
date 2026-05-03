from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import InscriptionForm, ConnexionForm
# Create your views here.

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta



def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecter l'utilisateur après inscription
            return redirect('accounts:connexion')
    else:
        form = InscriptionForm()

    return render(request, 'accounts/inscription.html', {'form': form})



def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = ConnexionForm()

    return render(request, 'accounts/connexion.html', {'form': form})


@login_required  # redirige vers la page de connexion si non connecté
def dashboard(request):
   return render(request, 'base.html')


@login_required
def dashboard_index(request):
    """Vue principale du dashboard avec statistiques"""
    from Demande.models import Demande
    from commande.models import Commande, Livraison
    from Fournisseur.models import Fournisseur
    from inventaire.models import Stock
    
    # Statistiques des demandes
    total_demandes = Demande.objects.count()
    demandes_en_cours = Demande.objects.filter(statut_demande='En cours').count()
    demandes_validees = Demande.objects.filter(statut_demande='Validée').count()
    
    # Statistiques des commandes
    total_commandes = Commande.objects.count()
    commandes_en_cours = Commande.objects.filter(statut_cmnd='en_cours').count()
    commandes_terminees = Commande.objects.filter(statut_cmnd='terminee').count()
    
    # Statistiques des fournisseurs
    total_fournisseurs = Fournisseur.objects.count()
    fournisseurs_actifs = Fournisseur.objects.filter(statut='Actif').count()
    
    # Statistiques du stock
    total_articles_stock = Stock.objects.count()
    articles_faible_stock = Stock.objects.filter(quantite_disponible__lte=5).count()
    
    # Livraisons récentes
    total_livraisons = Livraison.objects.count()
    
    # Dernières activités
    dernieres_demandes = Demande.objects.order_by('-date_demande')[:5]
    dernieres_commandes = Commande.objects.order_by('-date_ajout')[:5]
    
    context = {
        # Demandes
        'total_demandes': total_demandes,
        'demandes_en_cours': demandes_en_cours,
        'demandes_validees': demandes_validees,
        # Commandes
        'total_commandes': total_commandes,
        'commandes_en_cours': commandes_en_cours,
        'commandes_terminees': commandes_terminees,
        # Fournisseurs
        'total_fournisseurs': total_fournisseurs,
        'fournisseurs_actifs': fournisseurs_actifs,
        # Stock
        'total_articles_stock': total_articles_stock,
        'articles_faible_stock': articles_faible_stock,
        # Livraisons
        'total_livraisons': total_livraisons,
        # Activités récentes
        'dernieres_demandes': dernieres_demandes,
        'dernieres_commandes': dernieres_commandes,
        # Date du jour
        'today': timezone.now(),
    }
    
    return render(request, 'accounts/dashboard_index.html', context)



def deconnexion(request):
    logout(request)
    return redirect('accounts:connexion')

"""Vue de test pour envoyer un email via SendGrid."""
""""
def test_send_email(request):
    send_mail(
        "Test Email Django + SendGrid",            # Sujet
        "Ceci est un email de test envoyé depuis Django.",  # Message
        settings.DEFAULT_FROM_EMAIL,              # Expéditeur
        ["edenhavila2004@gmail.com"],             # Destinataire
        fail_silently=False,
    )
    return HttpResponse("Email envoyé !")
"""
