import json
from django.contrib import messages
from django.db import models
from django.db.models import Q
from django.http import request, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BienForm,ServiceForm
from .models import *
from django.contrib.auth.decorators import login_required


#---------------------------------------------------------------
# VUES POUR LES SERVICES    
#---------------------------------------------------------------
@login_required
def index_service(request):
    services = Service.objects.all()
    return render(request, 'Service/index_service.html', {'services': services})


@login_required
def liste_services(request):
    services = Service.objects.select_related('categorie').all()
    q = request.GET.get('q', '').strip()
    if q:
        services = services.filter(
            Q(reference__icontains=q) |
            Q(designation__icontains=q)
        )
    frequence = request.GET.get('frequence', '').strip()
    if frequence:
        services = services.filter(frequence=frequence)
    categorie = request.GET.get('categorie', '').strip()
    if categorie:
        services = services.filter(categorie_id=categorie)
    return render(request, "Service/partials/liste_services.html", {"services": services})


@login_required
def CreateUpdateServiceView(request, pk=None):
    if pk:
        service = get_object_or_404(Service, pk=pk)
        form = ServiceForm(request.POST or None, instance=service)
        button_text = "Modifier"
        is_editing = True
    else:
        service = None
        form = ServiceForm(request.POST or None)
        button_text = "Ajouter"
        is_editing = False

    if request.method == "POST":
        if form.is_valid():
            form.save()
            if is_editing:
                messages.info(request, "Service modifié avec succès .")
                response = render(request, 'Service/fragment_form.html')
                response["HX-Trigger"] = json.dumps({
                    "refresh-messages": True,
                    "update": True
                })
                return response
            else:
                form = ServiceForm()
                messages.success(request, "Service ajouté avec succès .")
                response = render(request, 'Service/fragment_form.html', {'form': form})
                response["HX-Trigger"] = "refresh-messages"
                return response

    return render(request, "Service/fragment_form.html", {
        "form": form,
        "service": service,
        "button_text": button_text,
        "is_editing": is_editing,
    })


@login_required
def detail_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'Service/fragment_detail.html', {'service': service})


#---------------------------------------------------------------
# VUES POUR LES SERVICES
#---------------------------------------------------------------
def index_service(request):
    services = Service.objects.all()
    return render(request, 'Service/index_service.html',{'services': services})




#---------------------------------------------------------------
# VUES POUR LES Biens   
#---------------------------------------------------------------
# Create your views here.
@login_required
def index_bien(request):
    biens = Bien.objects.all()
    return render(request, 'Bien/index.html',{'biens': biens})


#11/11/2025
#avoir un bouton"Ajouter un Bien/service" qui une fois cliqué fait apparatre le modale contenant le formulaire
#le formulaire du bien ou du service est masqué au préalable, celui ci apparait apres avoir sélectionné un champ contenant "Vide,Bien, Service"
#en fonction de la sélection, le formulaire adéquat apparaitra
#Apres validation du formulaire adequat le retour sera "Liste Biens/Services"
""""
def ajouter_bien(request):
    if request.method == 'POST':
        form = BienForm(request.POST)
        if form.is_valid():
            form.save()
            form = BienForm()
            messages.success(request, "Bien ajouté avec succès !")
            response = render(request, 'Bien/ajouter.html', {'form': form})
            response["HX-Trigger"] = "refresh-messages"
            return response
    else:
        form = BienForm()

    return render(request, 'Bien/ajouter.html', {'form': form})
"""

@login_required
def liste_biens(request):
    biens = Bien.objects.select_related('sous_categorie__categorie__famille').all()
    
    # Recherche par texte
    q = request.GET.get('q', '').strip()
    if q:
        biens = biens.filter(
            Q(reference__icontains=q) |
            Q(designation__icontains=q)
        )
    
    # Filtre par fréquence d'utilisation
    frequence = request.GET.get('frequence', '').strip()
    if frequence:
        biens = biens.filter(frequence_utilisation=frequence)
    
    # Filtre par sous-catégorie
    sous_categorie = request.GET.get('sous_categorie', '').strip()
    if sous_categorie:
        biens = biens.filter(sous_categorie_id=sous_categorie)
    
    return render(request, "Bien/partials/liste_biens.html", {"biens": biens})


@login_required
def liste_biens_services(request):
    return render(request, "catalogue/liste_biens_services.html")


@login_required
def CreateUpdateBienView(request, pk=None):
    if pk:
        bien = get_object_or_404(Bien, pk=pk)
        form = BienForm(request.POST or None, instance=bien)
        button_text = "Modifier"
        is_editing = True
    else:
        bien = None
        form = BienForm(request.POST or None)
        button_text = "Ajouter"
        is_editing = False

    if request.method == "POST":
        if form.is_valid():
            form.save()
            if is_editing:
                messages.info(request, "Bien modifié avec succès .")
                response = render(request, 'Bien/fragment_form.html', {
                    "form": BienForm(),
                    "bien": None,
                    "button_text": "Ajouter",
                    "is_editing": False,
                })
                response["HX-Trigger"] = json.dumps({
                    "refresh-messages": True,
                    "update": True,
                    "close-modal": True,
                })
                return response
            else:
                form = BienForm()
                messages.success(request, "Bien ajouté avec succès .")
                response = render(request, 'Bien/fragment_form.html', {
                    "form": form,
                    "bien": None,
                    "button_text": "Ajouter",
                    "is_editing": False,
                })
                response["HX-Trigger"] = json.dumps({
                    "refresh-messages": True,
                    "update": True,
                })
                return response

    return render(request, "Bien/fragment_form.html", {
        "form": form,
        "bien": bien,
        "button_text": button_text,
        "is_editing": is_editing,
    })


@login_required
def supprimer_bien(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    bien = get_object_or_404(Bien, pk=pk)
    bien.delete()
    return HttpResponse("")  # HTMX supprime l'élément ciblé


@login_required
def detail_bien(request, pk):
    """Vue pour afficher les détails d'un bien"""
    bien = get_object_or_404(Bien, pk=pk)
    return render(request, 'Bien/partials/fragment_detail.html', {'bien': bien})