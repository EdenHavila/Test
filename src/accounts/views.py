from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import InscriptionForm, ConnexionForm
from .models import User
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib import messages
# Create your views here.

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from accounts.permissions import is_demandeur



def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Créer l'utilisateur en mode non actif et envoyer un email d'activation
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = request.build_absolute_uri(
                    reverse('accounts:activate', args=[uid, token])
                )

                subject = "Activation de votre compte"
                message = (
                    f"Bonjour {user.first_name or user.username},\n\n"
                    "Merci de vous être inscrit. Pour activer votre compte, cliquez sur le lien suivant :\n\n"
                    f"{activation_link}\n\n"
                    "Si vous n'avez pas demandé cette inscription, ignorez cet email."
                )

                try:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                except Exception as e:
                    # Log en console (dev) et informer l'utilisateur
                    print('Erreur envoi email activation:', e)
                    messages.warning(request, "Inscription enregistrée mais l'email d'activation n'a pas pu être envoyé. Contactez un administrateur.")
                    return redirect('accounts:connexion')

                messages.success(request, "Inscription enregistrée. Vérifiez votre email pour activer votre compte.")
                return redirect('accounts:inscription_done')
            except Exception as e:
                print('Erreur lors de la création du user:', e)
                messages.error(request, 'Une erreur est survenue lors de votre inscription. Réessayez plus tard.')
        else:
            # Form invalid → afficher erreurs via template
            messages.error(request, 'Le formulaire contient des erreurs, veuillez vérifier.')
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
    """Vue principale du dashboard avec statistiques.

    Règle d'affichage:
    - Demandeur: uniquement les données liées à l'utilisateur connecté.
    - Gestionnaire/Admin: vue globale de l'application.
    """
    from Demande.models import Demande
    from commande.models import Commande, Livraison
    from Fournisseur.models import Fournisseur
    from inventaire.models import Stock

    is_demandeur_dashboard = is_demandeur(request.user)

    # Portée des données: personnelle pour Demandeur, globale sinon.
    if is_demandeur_dashboard:
        demandes_qs = Demande.objects.filter(utilisateur=request.user)
        commandes_qs = Commande.objects.filter(demande__utilisateur=request.user)
        livraisons_qs = Livraison.objects.filter(commande__demande__utilisateur=request.user)
        # Fournisseurs concernés par les commandes du demandeur.
        fournisseurs_qs = Fournisseur.objects.filter(commande__demande__utilisateur=request.user).distinct()
    else:
        demandes_qs = Demande.objects.all()
        commandes_qs = Commande.objects.all()
        livraisons_qs = Livraison.objects.all()
        fournisseurs_qs = Fournisseur.objects.all()
    
    # Statistiques des demandes
    total_demandes = demandes_qs.count()
    demandes_en_cours = demandes_qs.filter(statut_demande='En cours').count()
    demandes_validees = demandes_qs.filter(statut_demande='Validée').count()
    
    # Statistiques des commandes
    total_commandes = commandes_qs.count()
    commandes_en_cours = commandes_qs.filter(statut_cmnd='en_cours').count()
    commandes_terminees = commandes_qs.filter(statut_cmnd='terminee').count()
    
    # Statistiques des fournisseurs
    total_fournisseurs = fournisseurs_qs.count()
    fournisseurs_actifs = fournisseurs_qs.filter(statut='Actif').count()
    
    # Statistiques du stock
    # Le stock est global et non rattaché au Demandeur: on l'affiche uniquement
    # pour les profils avec vue globale.
    if is_demandeur_dashboard:
        total_articles_stock = 0
        articles_faible_stock = 0
    else:
        total_articles_stock = Stock.objects.count()
        articles_faible_stock = Stock.objects.filter(quantite_disponible__lte=5).count()
    
    # Livraisons récentes
    total_livraisons = livraisons_qs.count()
    
    # Dernières activités
    dernieres_demandes = demandes_qs.order_by('-date_demande')[:5]
    dernieres_commandes = commandes_qs.order_by('-date_ajout')[:5]
    
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
        # Utilisé dans le template pour masquer les blocs globaux.
        'is_demandeur_dashboard': is_demandeur_dashboard,
    }
    
    return render(request, 'accounts/dashboard_index.html', context)



def deconnexion(request):
    logout(request)
    return redirect('accounts:connexion')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:dashboard')
    else:
        return HttpResponse('Lien d\'activation invalide ou expiré.')

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
