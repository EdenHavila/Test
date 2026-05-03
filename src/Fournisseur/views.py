from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from monprojet.utils.limit_m2m_display import limit_m2m_display

#from django.http import JsonResponse, HttpResponseBadRequest
from .forms import *
#from catalogue.models import Bien, Service
from catalogue.models import SousCategorie

from .models import Fournisseur, Type

# Create your views here.
#pas utile
@login_required
def index(request):
    return render(request, 'Fournisseur/index.html')
"""
def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()  # Récupérer tous les articles
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'Fournisseur/liste_f.html', {'fournisseurs': fournisseurs})
    return HttpResponseBadRequest("Requête non autorisée.")

def get_biens_or_services(request):
    type = request.GET.get('specialite')  # 'bien' ou 'service'
    if type == 'Bien':
        biens = list(Bien.objects.all().values('id', 'designation'))
        return JsonResponse(biens, safe=False)
    elif type == 'Service':
        services = list(Service.objects.all().values('id', 'designation'))
        return JsonResponse(services, safe=False)
    return JsonResponse([], safe=False)
"""
"""
def ajouter_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Fournisseur:liste_fournisseurs')  # Remplace avec l'URL de succès
    else:
        form = FournisseurForm()

    return render(request, 'Fournisseur/liste_f.html', {'form': form})
"""
#def liste_fournisseurs(request):
    #fournisseurs = Fournisseur.objects.all()  # Récupérer tous les articles
    ##return render(request, 'Fournisseur/liste_fournisseurs.html', {'fournisseurs': fournisseurs})

@login_required
def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.prefetch_related('types', 'specialite').all()
    
    # Recherche par texte
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        fournisseurs = fournisseurs.filter(
            Q(reference__icontains=q) |
            Q(nom__icontains=q)
        )
    
    # Filtre par statut
    statut = request.GET.get('statut', '').strip()
    if statut:
        fournisseurs = fournisseurs.filter(statut=statut)
    
    # Filtre par type (Bien ou Service)
    type_filter = request.GET.get('type', '').strip()
    if type_filter:
        fournisseurs = fournisseurs.filter(types__nom=type_filter)
    
    return render(request, 'Fournisseur/partials/liste_fournisseurs.html', {'fournisseurs': fournisseurs})

@login_required
def CreateUpdateView(request, pk=None):
    if pk:
        fournisseur =get_object_or_404(Fournisseur, pk=pk)
        form = FournisseurForm(request.POST, instance=fournisseur)
        is_editing = True
        button_text = "Modifier"

    else:
        fournisseur = None
        form = FournisseurForm(request.POST or None)
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
                messages.info(request, "Fournisseur modifiée avec succès .")
                response = HttpResponse(status=204)
                #response = render(request, 'Fournisseur/partials/liste_fournisseurs.html')  # vers la page détail après modification
                #redirect_url = reverse("Fournisseur:index")
                #response["HX-Redirect"] = redirect_url # Redirection après modification
                response["HX-Location"] = json.dumps({#
                    "path": reverse("Fournisseur:index"),
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
                form = FournisseurForm()
                messages.success(request, "Fournisseur ajouté avec succès .")
                response = render(request, 'Fournisseur/form_fournisseur.html', {'form': form})
                response["HX-Trigger"] = "refresh-messages"  # trigger côté JS
                return response
            
        else:
            print("Form invalid:", form.errors)   
    else:
        form = FournisseurForm(instance=fournisseur)

    return render(request, 'Fournisseur/form_fournisseur.html', {
        'form': form,
        'is_editing': is_editing,
        'fournisseur': fournisseur,
        'button_text': button_text,
    })

@login_required
def supprimer_fournisseur(request, pk):
    """Vue pour supprimer un fournisseur via HTMX"""
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    
    if request.method == 'POST':
        fournisseur.delete()
        messages.success(request, "Fournisseur supprimé avec succès.")
        
        # Retourne une réponse vide pour que HTMX supprime la ligne du tableau
        response = HttpResponse("")
        response["HX-Trigger"] = "refresh-messages"
        return response
    
    # Si ce n'est pas une requête POST, retourner une erreur
    return HttpResponse(status=405)


@login_required
def detail_fournisseur(request, pk):
    """Vue pour afficher les détails d'un fournisseur dans une modale"""
    fournisseur = get_object_or_404(
        Fournisseur.objects.prefetch_related('types', 'specialite'),
        pk=pk
    )
    # Récupérer les 5 dernières commandes du fournisseur (si le modèle existe)
    commandes = None
    try:
        from commande.models import Commande
        commandes = Commande.objects.filter(fournisseur=fournisseur).order_by('-date_cmnd')[:5]
    except:
        pass
    
    return render(request, 'Fournisseur/partials/detail_fournisseur.html', {
        'fournisseur': fournisseur,
        'commandes': commandes
    })


@login_required
def  charger_specialite(request):
    type_fournisseur = request.GET.getlist("types") or request.GET.getlist("types[]") # ["BIEN", "SERVICE"]

    if not type_fournisseur:
        return HttpResponse("")
    else:
        sous_categories = SousCategorie.objects.filter(type__in=type_fournisseur)

        print(f"Types reçus : {type_fournisseur}")
        print(f"Nombre de sous-catégories trouvées : {sous_categories.count()}")
    html = render_to_string(
        "Fournisseur/partials/specialite_select.html",
        {"sous_categories": sous_categories}
    )
    return HttpResponse(html)
