from django.utils import timezone
from monprojet.utils.export_utils import build_csv_response, build_excel_response
from .models import Livraison


def _filtered_livraisons(request):
    """Construit la liste filtrée des livraisons."""
    livraisons = Livraison.objects.select_related('commande', 'commande__fournisseur').all().order_by('-date_enregistrement')

    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        livraisons = livraisons.filter(
            Q(code_livraison__icontains=q) |
            Q(commande__code_cmnd__icontains=q)
        )

    statut = request.GET.get('statut', '').strip()
    if statut:
        livraisons = livraisons.filter(statut=statut)

    date_debut = request.GET.get('date_debut', '').strip()
    if date_debut:
        livraisons = livraisons.filter(date_livraison__gte=date_debut)

    date_fin = request.GET.get('date_fin', '').strip()
    if date_fin:
        livraisons = livraisons.filter(date_livraison__lte=date_fin)

    return livraisons



def _livraison_rows(livraisons):
    """Prépare les lignes d'export pour les livraisons."""
    return [
        [
            livraison.code_livraison,
            livraison.commande.code_cmnd if livraison.commande else '-',
            livraison.commande.fournisseur.nom if livraison.commande and livraison.commande.fournisseur else '-',
            livraison.date_livraison.strftime('%d/%m/%Y') if livraison.date_livraison else '-',
            livraison.date_enregistrement.strftime('%d/%m/%Y %H:%M') if livraison.date_enregistrement else '-',
            livraison.get_statut_display() if hasattr(livraison, 'get_statut_display') else livraison.statut,
            livraison.observation or '-',
        ]
        for livraison in livraisons
    ]



def export_livraisons_csv(request):
    """Exporte la liste filtrée des livraisons au format CSV."""
    livraisons = _filtered_livraisons(request)
    headers = ["Code", "Commande", "Fournisseur", "Date livraison", "Enregistré le", "Statut", "Observation"]
    filename = f"livraisons_{timezone.now():%Y%m%d_%H%M}.csv"
    return build_csv_response(filename, headers, _livraison_rows(livraisons))



def export_livraisons_excel(request):
    """Exporte la liste filtrée des livraisons au format Excel."""
    livraisons = _filtered_livraisons(request)
    headers = ["Code", "Commande", "Fournisseur", "Date livraison", "Enregistré le", "Statut", "Observation"]
    filename = f"livraisons_{timezone.now():%Y%m%d_%H%M}.xlsx"
    return build_excel_response(filename, "Livraisons", headers, _livraison_rows(livraisons))
