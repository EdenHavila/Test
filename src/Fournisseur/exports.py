from django.utils import timezone
from monprojet.utils.export_utils import build_csv_response, build_excel_response
from .models import Fournisseur


def _filtered_fournisseurs(request):
    """Construit la liste des fournisseurs à partir des filtres visibles à l'écran."""
    fournisseurs = Fournisseur.objects.prefetch_related('types', 'specialite').all().order_by('nom')

    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        fournisseurs = fournisseurs.filter(
            Q(reference__icontains=q) |
            Q(nom__icontains=q) |
            Q(email__icontains=q)
        )

    statut = request.GET.get('statut', '').strip()
    if statut:
        fournisseurs = fournisseurs.filter(statut=statut)

    type_filter = request.GET.get('type', '').strip()
    if type_filter:
        fournisseurs = fournisseurs.filter(types__nom=type_filter)

    return fournisseurs.distinct()


def _fournisseur_rows(fournisseurs):
    """Prépare les lignes d'export pour les fournisseurs."""
    return [
        [
            fournisseur.reference,
            fournisseur.nom,
            fournisseur.email or '-',
            fournisseur.telephone or '-',
            fournisseur.adresse or '-',
            fournisseur.statut,
            ", ".join(t.nom for t in fournisseur.types.all()) or '-',
            ", ".join(s.nom for s in fournisseur.specialite.all()) or '-',
        ]
        for fournisseur in fournisseurs
    ]



def export_fournisseurs_csv(request):
    """Exporte la liste filtrée des fournisseurs au format CSV."""
    fournisseurs = _filtered_fournisseurs(request)
    headers = ["Référence", "Nom", "Email", "Téléphone", "Adresse", "Statut", "Types", "Spécialités"]
    filename = f"fournisseurs_{timezone.now():%Y%m%d_%H%M}.csv"
    return build_csv_response(filename, headers, _fournisseur_rows(fournisseurs))



def export_fournisseurs_excel(request):
    """Exporte la liste filtrée des fournisseurs au format Excel."""
    fournisseurs = _filtered_fournisseurs(request)
    headers = ["Référence", "Nom", "Email", "Téléphone", "Adresse", "Statut", "Types", "Spécialités"]
    filename = f"fournisseurs_{timezone.now():%Y%m%d_%H%M}.xlsx"
    return build_excel_response(filename, "Fournisseurs", headers, _fournisseur_rows(fournisseurs))
