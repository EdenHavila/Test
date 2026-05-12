import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
#from django.forms import modelformset_factory
from .models import Demande
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseForbidden
from accounts.permissions import (
    is_admin,
    is_gestionnaire,
    is_demandeur,
    any_role_required,
)
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET




# Vue HTMX pour ajouter dynamiquement une ligne de DetailsDemande
@login_required
@require_GET
def ligne_add(request):
    """Retourne un fragment HTML pour une nouvelle ligne de DetailsDemande (formset)"""
    form_idx = int(request.GET.get('form_idx', 0))
    formset = FormSetDetailsDemande(prefix='lignes')
    empty_form = formset.empty_form
    empty_form.prefix = f'lignes-{form_idx}'
    html = render_to_string('Demande/partials/ligne_details_demande.html', {'form': empty_form, 'form_idx': form_idx})
    return HttpResponse(html)

#A créer
#liste demande,
# Create your views here.
#FormSetDetailsDemande = modelformset_factory(DetailsDemande, form=DetailsDemandeForm, extra=1, can_delete=True)

@login_required
@any_role_required
def index(request):
    """Index des demandes.

    Accessible aux utilisateurs participant au flux de demandes
    (Demandeur, Gestionnaire, Admin). Le contrôle protège la page
    côté serveur (le template masque aussi les liens).
    """
    return render(request, 'Demande/index.html')

"""
def ajouter_demande(request):
    if request.method == 'POST':
        form = DemandeForm(request.POST,request.FILES)
        form_set=FormSetDetailsDemande(request.POST,queryset=DetailsDemande.objects.none())
        if form.is_valid() and form_set.is_valid():
            demande=form.save()

            for form in form_set:
                if form.cleaned_data:
                    details_demande = form.save(commit=False)
                    details_demande.demande = demande  # Associer l'étudiant fraîchement créé
                    details_demande.save()


            return redirect('Demande:index')  # Remplace avec l'URL de succès
    else:
        form = DemandeForm()
        form_set=FormSetDetailsDemande(queryset=DetailsDemande.objects.none())


    return render(request, 'Demande/form_demande.html', {'form': form,'form_set':form_set})
"""


@login_required
def charge_champ_demandes(request):
    """Vue HTMX : recharge le fragment demandes_associees selon type_demande."""
    data = request.GET.copy()
    # Dédupliquer type_demande si envoyé plusieurs fois
    type_list = data.getlist('type_demande')
    if type_list:
        data.setlist('type_demande', [type_list[-1]])
    
    # DEBUG - À SUPPRIMER APRÈS
    type_val = data.get('type_demande', '')
    groups = list(request.user.groups.values_list('name', flat=True))
    print(f"[DEBUG VUE] user={request.user}, groups={groups}, type_demande='{type_val}'")
    
    form = DemandeForm(data, user=request.user)
    
    # DEBUG - À SUPPRIMER APRÈS
    print(f"[DEBUG VUE] form.fields = {list(form.fields.keys())}")
    print(f"[DEBUG VUE] demandes_associees present = {'demandes_associees' in form.fields}")
    
    html = render_to_string("Demande/partials/champ_demandes_associees.html", {"form": form}, request=request)
    
    # DEBUG - À SUPPRIMER APRÈS
    print(f"[DEBUG VUE] HTML length = {len(html)} bytes")
    print(f"[DEBUG VUE] HTML content = {repr(html[:200])}")
    
    return HttpResponse(html)

@login_required
@any_role_required
def liste(request):
    demandes = Demande.objects.all().order_by('-pk')
    
    # Recherche par texte
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        demandes = demandes.filter(
            Q(code_demande__icontains=q) |
            Q(motif_demande__icontains=q)
        )
    
    # Filtre par type de demande
    type_demande = request.GET.get('type_demande', '').strip()
    if type_demande:
        demandes = demandes.filter(type_demande=type_demande)
    
    # Filtre par nature de demande
    nature_demande = request.GET.get('nature_demande', '').strip()
    if nature_demande:
        demandes = demandes.filter(nature_demande=nature_demande)
    
    # Filtre par statut
    statut_demande = request.GET.get('statut_demande', '').strip()
    if statut_demande:
        demandes = demandes.filter(statut_demande=statut_demande)
    
    # Filtre par date de début
    date_debut = request.GET.get('date_debut', '').strip()
    if date_debut:
        demandes = demandes.filter(date_demande__gte=date_debut)
    
    # Filtre par date de fin
    date_fin = request.GET.get('date_fin', '').strip()
    if date_fin:
        demandes = demandes.filter(date_demande__lte=date_fin)
    
    return render(request, 'Demande/partials/liste.html', {'demandes': demandes})


@login_required
@any_role_required
def mes_demandes_index(request):
    """Page 'Mes demandes'.

    Visible par tous les rôles métiers; dans les templates/partials la
    liste effective est filtrée (voir `mes_demandes_liste`).
    """
    return render(request, 'Demande/mes_demandes.html')


@login_required
@any_role_required
def mes_demandes_liste(request):
    """Vue pour afficher uniquement les demandes de l'utilisateur connecté"""
    # Filtrer par l'utilisateur connecté
    demandes = Demande.objects.filter(utilisateur=request.user).order_by('-pk')
    
    # Recherche par texte
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        demandes = demandes.filter(
            Q(code_demande__icontains=q) |
            Q(motif_demande__icontains=q)
        )
    
    # Filtre par nature de demande
    nature_demande = request.GET.get('nature_demande', '').strip()
    if nature_demande:
        demandes = demandes.filter(nature_demande=nature_demande)
    
    # Filtre par statut
    statut_demande = request.GET.get('statut_demande', '').strip()
    if statut_demande:
        demandes = demandes.filter(statut_demande=statut_demande)
    
    # Filtre par date de début
    date_debut = request.GET.get('date_debut', '').strip()
    if date_debut:
        demandes = demandes.filter(date_demande__gte=date_debut)
    
    # Filtre par date de fin
    date_fin = request.GET.get('date_fin', '').strip()
    if date_fin:
        demandes = demandes.filter(date_demande__lte=date_fin)
    
    return render(request, 'Demande/partials/liste_mes_demandes.html', {'demandes': demandes})


@login_required
def CreateUpdateView(request, pk=None):
    if pk:
        demande = get_object_or_404(Demande, pk=pk)
        is_editing = True
        action = 'Modifier'
    else:
        demande = None
        is_editing = False
        action = 'Enregistrer'

    # Permission: edition autorisée pour Admin/Gestionnaire ou propriétaire
    if is_editing:
        if not (is_admin(request.user) or is_gestionnaire(request.user) or demande.utilisateur == request.user):
            return HttpResponseForbidden("Vous n'avez pas la permission de modifier cette demande.")

    if request.method == 'POST':
        form = DemandeForm(request.POST, request.FILES, instance=demande, user=request.user)
        formset = FormSetDetailsDemande(request.POST, instance=demande, prefix='lignes')
        
        if form.is_valid() and formset.is_valid():
            demande_obj = form.save(commit=False)
            # Associer l'utilisateur connecté à la demande lors de la création
            if not is_editing:
                demande_obj.utilisateur = request.user
            demande_obj.save()
            form.save_m2m()  # Sauvegarder les relations ManyToMany (demandes_associees)
            
            formset.instance = demande_obj
            formset.save()
            
            # Message de succès
            if is_editing:
                messages.success(request, "Demande modifiée avec succès.")
            else:
                messages.success(request, "Demande créée avec succès.")
            
            response = HttpResponse()
            response['HX-Trigger'] = 'refresh-messages, close-modal, refresh-list'
            return response
        else:
            # Debug : afficher les erreurs en console
            print(f"[DEBUG] Form errors: {form.errors}")
            print(f"[DEBUG] Formset errors: {formset.errors}")
    else:
        form = DemandeForm(instance=demande, user=request.user)
        formset = FormSetDetailsDemande(instance=demande, prefix='lignes')

    context = {
        'form': form,
        'formset': formset,
        'demande': demande,
        'is_editing': is_editing,
        'action': action,
    }
    return render(request, 'Demande/fragment_form.html', context)


@login_required
def supprimer_demande(request, pk):
    """Vue pour supprimer une demande via HTMX"""
    demande = get_object_or_404(Demande, pk=pk)
    
    # Permission: seul l'admin, le gestionnaire ou le propriétaire peut supprimer
    if not (is_admin(request.user) or is_gestionnaire(request.user) or demande.utilisateur == request.user):
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer cette demande.")

    if request.method == 'POST':
        demande.delete()
        messages.success(request, "Demande supprimée avec succès.")
        # Retourne une réponse vide pour que HTMX supprime la ligne du tableau
        response = HttpResponse("")
        response["HX-Trigger"] = "refresh-messages"
        return response

    # Si ce n'est pas une requête POST, retourner une erreur
    return HttpResponse(status=405)


@login_required
def detail_demande(request, pk):
    """Vue pour afficher les détails d'une demande via HTMX"""
    demande = get_object_or_404(Demande, pk=pk)
    
    # Récupérer les lignes de détails de la demande
    lignes = demande.detailsdemande_set.all()
    
    # Récupérer les demandes associées (pour les demandes de type Gestionnaire)
    demandes_associees = demande.demandes_associees.all()
    
    # Récupérer les demandes qui regroupent cette demande (si type Demandeur)
    regroupee_par = demande.regroupee_par.all()
    
    # Permission: gestionnaire/admin peuvent voir toutes les demandes,
    # un demandeur ne peut voir que ses propres demandes.
    if is_demandeur(request.user) and demande.utilisateur != request.user:
        return HttpResponseForbidden("Accès refusé")

    context = {
        'demande': demande,
        'lignes': lignes,
        'demandes_associees': demandes_associees,
        'regroupee_par': regroupee_par,
    }
    return render(request, 'Demande/partials/detail_demande.html', context)
