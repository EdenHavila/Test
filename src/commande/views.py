from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from catalogue.models import Bien, Service
from .models import Commande, LigneCommande, Livraison
from .forms import CommandeForm, LigneCommandeForm, LigneCommandeFormSet, LivraisonForm
from django.contrib.auth.decorators import login_required
from monprojet.utils.export_utils import (
    build_csv_response,
    build_excel_response,
)

# Create your views here.
#----------------------------------------------------------------------------------------------
# VUES POUR LA GESTION DES COMMANDES    

@login_required
def index_commande(request):
    return render(request, 'Commande/index.html')

@login_required
def liste_commandes(request):
    commandes = _get_filtered_commandes(request)
    return render(request, 'Commande/partials/liste_commandes.html', {'commandes': commandes})


def _get_filtered_commandes(request):
    """Construit la liste des commandes à partir des filtres visibles à l'écran."""
    commandes = Commande.objects.all().select_related('demande', 'fournisseur').order_by('-date_ajout')

    # Recherche par texte
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        commandes = commandes.filter(
            Q(code_cmnd__icontains=q) |
            Q(fournisseur__nom__icontains=q)
        )

    # Filtre par statut
    statut = request.GET.get('statut', '').strip()
    if statut:
        commandes = commandes.filter(statut_cmnd=statut)

    # Filtre par date de début
    date_debut = request.GET.get('date_debut', '').strip()
    if date_debut:
        commandes = commandes.filter(date_cmnd__gte=date_debut)

    # Filtre par date de fin
    date_fin = request.GET.get('date_fin', '').strip()
    if date_fin:
        commandes = commandes.filter(date_cmnd__lte=date_fin)

    return commandes


def _commandes_export_rows(commandes):
    """Prépare les lignes d'export pour les commandes."""
    return [
        [
            commande.code_cmnd,
            commande.demande.code_demande if commande.demande else '-',
            commande.fournisseur.nom if commande.fournisseur else '-',
            commande.date_cmnd.strftime('%d/%m/%Y') if commande.date_cmnd else '-',
            commande.nombre_lignes,
            f"{commande.montant_total:.2f} FCFA" if commande.montant_total else '-',
            commande.get_statut_cmnd_display(),
        ]
        for commande in commandes
    ]


@login_required
def export_commandes_csv(request):
    """Exporte la liste filtrée des commandes au format CSV."""
    commandes = _get_filtered_commandes(request)
    headers = ["Code", "Demande", "Fournisseur", "Date commande", "Nombre d'articles", "Montant total", "Statut"]
    filename = f"commandes_{timezone.now():%Y%m%d_%H%M}.csv"
    return build_csv_response(filename, headers, _commandes_export_rows(commandes))


@login_required
def export_commandes_excel(request):
    """Exporte la liste filtrée des commandes au format Excel."""
    commandes = _get_filtered_commandes(request)
    headers = ["Code", "Demande", "Fournisseur", "Date commande", "Nombre d'articles", "Montant total", "Statut"]
    filename = f"commandes_{timezone.now():%Y%m%d_%H%M}.xlsx"
    return build_excel_response(filename, "Commandes", headers, _commandes_export_rows(commandes))


@login_required
def CreateUpdateView_commande(request, pk=None):
    """Vue unique pour créer ou modifier une commande avec ses lignes"""
    if pk:
        commande = get_object_or_404(Commande, pk=pk)
        is_editing = True
        action = 'Modifier'
    else:
        commande = None
        is_editing = False
        action = 'Enregistrer'

    if request.method == 'POST':
        form = CommandeForm(request.POST, request.FILES, instance=commande)
        formset = LigneCommandeFormSet(request.POST, instance=commande, prefix='lignes')
        
        if form.is_valid() and formset.is_valid():
            commande_obj = form.save()
            formset.instance = commande_obj
            formset.save()
            
            # Réponse HTMX pour fermer le modal et rafraîchir la liste
            response = HttpResponse()
            response['HX-Trigger'] = 'refresh-messages, close-modal'
            return response
    else:
        form = CommandeForm(instance=commande)
        formset = LigneCommandeFormSet(instance=commande, prefix='lignes')
    
    context = {
        'form': form,
        'formset': formset,
        'commande': commande,
        'is_editing': is_editing,
        'action': action,
    }
    return render(request, 'Commande/fragment_form.html', context)



@login_required
def supprimer_commande(request, pk):
    """Vue pour supprimer une commande"""
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        commande.delete()
        response = HttpResponse("")
        response['HX-Trigger'] = 'refresh-messages'
        return response
    return HttpResponse(status=405)



@login_required
def detail_commande(request, pk):
    """Vue pour afficher les détails d'une commande avec ses lignes"""
    commande = get_object_or_404(Commande, pk=pk)
    lignes = commande.lignes.all().select_related('bien', 'service')
    
    context = {
        'commande': commande,
        'lignes': lignes,
    }
    return render(request, 'Commande/partials/detail_commande.html', context)


# VUES HTMX POUR LES LIGNES DE COMMANDE
@login_required
def commande_ligne_add(request):
    """Ajoute une nouvelle ligne de formulaire vide"""
    # Récupérer l'index actuel des formulaires
    form_idx = request.GET.get('form_idx', 0)
    try:
        form_idx = int(form_idx)
    except ValueError:
        form_idx = 0
    
    # Créer un nouveau formulaire avec le bon préfixe
    form = LigneCommandeForm(prefix=f'lignes-{form_idx}')
    
    context = {
        'form': form,
        'form_idx': form_idx,
    }
    return render(request, 'Commande/partials/ligne_form.html', context)



@login_required
def commande_ligne_delete(request):
    """Supprime une ligne de formulaire (côté client seulement)"""
    # Cette vue retourne simplement une réponse vide pour que HTMX supprime l'élément
    return HttpResponse('')


@login_required
def charger_items(request):
    """Charge dynamiquement les biens ou services selon le type sélectionné"""
    type_item = request.GET.get('type', '')
    form_prefix = request.GET.get('prefix', '')
    
    # Debug: afficher les paramètres reçus
    print(f"[charger_items] type={type_item}, prefix={form_prefix}")
    print(f"[charger_items] GET params: {dict(request.GET)}")
    
    if type_item == 'Bien':
        items = Bien.objects.all().order_by('designation')
        template = 'Commande/partials/bien_select.html'
    elif type_item == 'Service':
        items = Service.objects.all().order_by('designation')
        template = 'Commande/partials/service_select.html'
    else:
        # Retourner un select désactivé si aucun type sélectionné
        return HttpResponse(f'''
            <select class="form-select" disabled>
                <option value="">-- Choisir d'abord un type --</option>
            </select>
            <input type="hidden" name="{form_prefix}-bien" value="">
            <input type="hidden" name="{form_prefix}-service" value="">
        ''')
    
    context = {
        'items': items,
        'prefix': form_prefix,
    }
    return render(request, template, context)

#----------------------------------------------------------------------------------------------
# VUES POUR LA GESTION DES LIVRAISONS
#----------------------------------------------------------------------------------------------
@login_required
def index_livraison(request):
    """Page principale des livraisons"""
    return render(request, 'Livraison/index.html')

@login_required
def liste_livraisons(request):
    """Liste des livraisons pour le chargement HTMX"""
    livraisons = Livraison.objects.all().select_related('commande', 'commande__fournisseur')
    
    # Recherche par texte
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        livraisons = livraisons.filter(
            Q(code_livraison__icontains=q) |
            Q(commande__code_cmnd__icontains=q)
        )
    
    # Filtre par statut
    statut = request.GET.get('statut', '').strip()
    if statut:
        livraisons = livraisons.filter(statut_livraison=statut)
    
    # Filtre par date de début
    date_debut = request.GET.get('date_debut', '').strip()
    if date_debut:
        livraisons = livraisons.filter(date_livraison__gte=date_debut)
    
    # Filtre par date de fin
    date_fin = request.GET.get('date_fin', '').strip()
    if date_fin:
        livraisons = livraisons.filter(date_livraison__lte=date_fin)
    
    return render(request, 'Livraison/partials/liste_livraisons.html', {'livraisons': livraisons})



@login_required
def CreateUpdateView_livraison(request, pk=None):
    """Vue unique pour créer ou modifier une livraison"""
    if pk:
        livraison = get_object_or_404(Livraison, pk=pk)
        is_editing = True
        action = 'Modifier'
    else:
        livraison = None
        is_editing = False
        action = 'Enregistrer'

    if request.method == 'POST':
        form = LivraisonForm(request.POST, request.FILES, instance=livraison)
        
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response['HX-Trigger'] = 'refresh-messages, close-modal'
            return response
    else:
        form = LivraisonForm(instance=livraison)
    
    context = {
        'form': form,
        'livraison': livraison,
        'is_editing': is_editing,
        'action': action,
    }
    return render(request, 'Livraison/fragment_form.html', context)



@login_required
def detail_livraison(request, pk):
    """Vue pour afficher les détails d'une livraison"""
    livraison = get_object_or_404(Livraison.objects.select_related('commande', 'commande__fournisseur', 'commande__demande'), pk=pk)
    
    context = {
        'livraison': livraison,
    }
    return render(request, 'Livraison/partials/detail_livraison.html', context)



@login_required
def supprimer_livraison(request, pk):
    """Vue pour supprimer une livraison"""
    livraison = get_object_or_404(Livraison, pk=pk)
    if request.method == 'POST':
        livraison.delete()
        response = HttpResponse("")
        response['HX-Trigger'] = 'refresh-messages'
        return response
    return HttpResponse(status=405)

