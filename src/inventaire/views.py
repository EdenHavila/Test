from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
import json

# Create your views here.
@login_required
def index_stock(request):
    return render(request, 'Stock/index.html')

def liste_stock(request):
    stocks = Stock.objects.select_related('bien', 'responsable_stock').all()
    
    # Recherche par texte
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        stocks = stocks.filter(
            Q(code__icontains=q) |
            Q(bien__designation__icontains=q)
        )
    
    # Filtre par lieu de stockage
    lieu = request.GET.get('lieu', '').strip()
    if lieu:
        stocks = stocks.filter(lieu_stockage=lieu)
    
    # Filtre par statut
    statut = request.GET.get('statut', '').strip()
    if statut:
        stocks = stocks.filter(statut_bien=statut)
    
    # Filtre par unité
    unite = request.GET.get('unite', '').strip()
    if unite:
        stocks = stocks.filter(unite=unite)
    
    # Filtre par date de début (date de mise à jour)
    date_debut = request.GET.get('date_debut', '').strip()
    if date_debut:
        stocks = stocks.filter(date_mise_a_jour__date__gte=date_debut)
    
    # Filtre par date de fin
    date_fin = request.GET.get('date_fin', '').strip()
    if date_fin:
        stocks = stocks.filter(date_mise_a_jour__date__lte=date_fin)
    
    return render(request, 'Stock/partials/liste_stock.html', {'stocks': stocks})   


@login_required
def CreateUpdateView_stock(request, pk=None):
    if pk:
        stock =get_object_or_404(Stock, pk=pk)
        form = StockForm(request.POST, instance=stock)
        is_editing = True
        button_text = "Modifier"
    else:
        stock = None
        form = StockForm(request.POST or None)
        button_text = "Ajouter"
        is_editing = False

    if request.method == 'POST':
        #form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            # Redirection conditionnelle
            # CAS 1 : Modification → redirection automatique vers la page de détails de l'élément question
            if is_editing:
                #redirect_url = reverse("Fournisseur:index") # URL de redirection après modification 
                messages.info(request, "Stock modifié avec succès .")
                response = HttpResponse(status=204)
                #response = render(request, 'Fournisseur/partials/liste_fournisseurs.html')  # vers la page détail après modification
                #redirect_url = reverse("Fournisseur:index")
                #response["HX-Redirect"] = redirect_url # Redirection après modification
                response["HX-Location"] = json.dumps({#
                    "path": reverse("inventaire:index-stock"),
                    "target": "#content-wrapper",
                    "swap": "innerHTML"
                })
                response["HX-Trigger"] = json.dumps({
                    "refresh-messages": True,
                    "update": True,
                    "close-modal": True,#pour fermer la modale après modification
                })  # trigger côté JS
                return response
            # CAS 2 : Ajout → rester dans la modale
            else:         
                form = StockForm()
                messages.success(request, "Stock ajouté avec succès .")
                response = render(request, 'Stock/fragment_form.html', {'form': form})
                response["HX-Trigger"] = "refresh-messages"  # trigger côté JS
                return response
            
        else:
            print("Form invalid:", form.errors)   
    else:
        form = StockForm(instance=stock)

    return render(request, 'Stock/fragment_form.html', {
        'form': form,
        'is_editing': is_editing,
        'stock': stock,
        'button_text': button_text,
    })

def supprimer_stock(request, pk):
    """Vue pour supprimer un stock via HTMX"""
    stock = get_object_or_404(Stock, pk=pk)
    
    if request.method == 'POST':
        stock.delete()
        messages.success(request, "Stock supprimé avec succès.")
        
        # Retourne une réponse vide pour que HTMX supprime la ligne du tableau
        response = HttpResponse("")
        response["HX-Trigger"] = "refresh-messages"
        return response
    
    # Si ce n'est pas une requête POST, retourner une erreur
    return HttpResponse(status=405)


@login_required
def detail_stock(request, pk):
    """Vue pour afficher les détails d'un stock dans une modale"""
    stock = get_object_or_404(
        Stock.objects.select_related('bien', 'responsable_stock'),
        pk=pk
    )
    # Récupérer les 10 derniers mouvements liés à ce stock
    mouvements = stock.mouvements.select_related('responsable').order_by('-date_mouvement')[:10]
    
    return render(request, 'Stock/partials/detail_stock.html', {
        'stock': stock,
        'mouvements': mouvements
    })    


#--------------------------------------------------------------
# VUES POUR LES MOUVEMENTS LOGISTIQUES
#--------------------------------------------------------------

@login_required
def index_mouvement(request):   
    return render(request, 'Mouvement/index.html')  

def liste_mouvement(request):
    mouvements = MouvementLogistique.objects.select_related('stock', 'stock__bien', 'responsable').all()
    
    # Recherche par texte (code, bien, destination, type de destination)
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        mouvements = mouvements.filter(
            Q(code__icontains=q) |
            Q(stock__bien__designation__icontains=q) |
            Q(destination__icontains=q) |
            Q(destination_type__icontains=q)
        )
    
    # Filtre par type de mouvement
    type_mouvement = request.GET.get('type_mouvement', '').strip()
    if type_mouvement:
        mouvements = mouvements.filter(type_mouvement=type_mouvement)
    
    # Filtre par source
    source = request.GET.get('source', '').strip()
    if source:
        mouvements = mouvements.filter(source=source)
    
    # Filtre par date de début
    date_debut = request.GET.get('date_debut', '').strip()
    if date_debut:
        mouvements = mouvements.filter(date_mouvement__date__gte=date_debut)
    
    # Filtre par date de fin
    date_fin = request.GET.get('date_fin', '').strip()
    if date_fin:
        mouvements = mouvements.filter(date_mouvement__date__lte=date_fin)
    
    return render(request, 'Mouvement/partials/liste_mouvement.html', {'mouvements': mouvements})   


@login_required
def CreateUpdateView_mouvement(request, pk=None):
    if pk:
        mouvement = get_object_or_404(MouvementLogistique, pk=pk)
        is_editing = True
        button_text = "Modifier"
    else:
        mouvement = None
        button_text = "Ajouter"
        is_editing = False

    if request.method == 'POST':
        form = MouvementLogistiqueForm(request.POST, request.FILES, instance=mouvement, user=request.user)
        if form.is_valid():
            mouvement_obj = form.save(commit=False)
            # Assigner le responsable car le champ est disabled
            mouvement_obj.responsable = request.user
            mouvement_obj.save()
            
            # Vérifier si une alerte de stock a été déclenchée
            if hasattr(mouvement_obj, '_alerte_stock') and mouvement_obj._alerte_stock:
                messages.warning(request, mouvement_obj._alerte_stock)
            
            if is_editing:
                messages.info(request, "Mouvement modifié avec succès .")
                response = HttpResponse(status=204)
                response["HX-Location"] = json.dumps({
                    "path": reverse("inventaire:index-mouvement"),
                    "target": "#content-wrapper",
                    "swap": "innerHTML"
                })
                response["HX-Trigger"] = json.dumps({
                    "refresh-messages": True,
                    "update": True,
                    "close-modal": True,
                })
                return response
            else:         
                form = MouvementLogistiqueForm(user=request.user)
                messages.success(request, "Mouvement ajouté avec succès .")
                response = render(request, 'Mouvement/fragment_form.html', {'form': form})
                response["HX-Trigger"] = "refresh-messages"
                return response
            
        else:
            print("Form invalid:", form.errors)   
    else:
        form = MouvementLogistiqueForm(instance=mouvement, user=request.user)

    return render(request, 'Mouvement/fragment_form.html', {
        'form': form,
        'is_editing': is_editing,
        'mouvement': mouvement,
        'button_text': button_text,
    })

def supprimer_mouvement(request, pk):
    """Vue pour supprimer un mouvement via HTMX"""
    mouvement = get_object_or_404(MouvementLogistique, pk=pk)
    
    if request.method == 'POST':
        mouvement.delete()
        messages.success(request, "Mouvement supprimé avec succès.")
        
        # Retourne une réponse vide pour que HTMX supprime la ligne du tableau
        response = HttpResponse("")
        response["HX-Trigger"] = "refresh-messages"
        return response
    
    # Si ce n'est pas une requête POST, retourner une erreur
    return HttpResponse(status=405)


@login_required
def detail_mouvement(request, pk):
    """Vue pour afficher les détails d'un mouvement dans une modale"""
    mouvement = get_object_or_404(
        MouvementLogistique.objects.select_related('stock', 'stock__bien', 'responsable'),
        pk=pk
    )
    return render(request, 'Mouvement/partials/detail_mouvement.html', {'mouvement': mouvement})


