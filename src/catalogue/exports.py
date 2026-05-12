from django.utils import timezone
from monprojet.utils.export_utils import build_csv_response, build_excel_response
from .models import Bien, Service


def _filtered_biens(request):
    """Construit la liste filtrée des biens."""
    biens = Bien.objects.select_related('sous_categorie__categorie__famille').all().order_by('reference')

    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        biens = biens.filter(
            Q(reference__icontains=q) |
            Q(designation__icontains=q) |
            Q(marque__icontains=q) |
            Q(modele__icontains=q)
        )

    frequence = request.GET.get('frequence', '').strip()
    if frequence:
        biens = biens.filter(frequence_utilisation=frequence)

    sous_categorie = request.GET.get('sous_categorie', '').strip()
    if sous_categorie:
        biens = biens.filter(sous_categorie_id=sous_categorie)

    return biens



def _filtered_services(request):
    """Construit la liste filtrée des services."""
    services = Service.objects.select_related('categorie__famille').all().order_by('reference')

    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        services = services.filter(
            Q(reference__icontains=q) |
            Q(designation__icontains=q) |
            Q(description__icontains=q)
        )

    frequence = request.GET.get('frequence', '').strip()
    if frequence:
        services = services.filter(frequence=frequence)

    categorie = request.GET.get('categorie', '').strip()
    if categorie:
        services = services.filter(categorie_id=categorie)

    return services



def _bien_rows(biens):
    """Prépare les lignes d'export pour les biens."""
    return [
        [
            bien.reference,
            bien.sous_categorie.nom if bien.sous_categorie else '-',
            bien.sous_categorie.categorie.designation if bien.sous_categorie and bien.sous_categorie.categorie else '-',
            bien.sous_categorie.categorie.famille.designation if bien.sous_categorie and bien.sous_categorie.categorie and bien.sous_categorie.categorie.famille else '-',
            bien.designation,
            bien.marque or '-',
            bien.modele or '-',
            bien.get_frequence_utilisation_display() if hasattr(bien, 'get_frequence_utilisation_display') else bien.frequence_utilisation,
        ]
        for bien in biens
    ]



def _service_rows(services):
    """Prépare les lignes d'export pour les services."""
    return [
        [
            service.reference,
            service.categorie.designation if service.categorie else '-',
            service.categorie.famille.designation if service.categorie and service.categorie.famille else '-',
            service.designation,
            service.get_frequence_display() if hasattr(service, 'get_frequence_display') else service.frequence,
            service.description,
        ]
        for service in services
    ]



def export_biens_csv(request):
    """Exporte la liste filtrée des biens au format CSV."""
    biens = _filtered_biens(request)
    headers = ["Référence", "Sous-catégorie", "Catégorie", "Famille", "Désignation", "Marque", "Modèle", "Fréquence"]
    filename = f"biens_{timezone.now():%Y%m%d_%H%M}.csv"
    return build_csv_response(filename, headers, _bien_rows(biens))



def export_biens_excel(request):
    """Exporte la liste filtrée des biens au format Excel."""
    biens = _filtered_biens(request)
    headers = ["Référence", "Sous-catégorie", "Catégorie", "Famille", "Désignation", "Marque", "Modèle", "Fréquence"]
    filename = f"biens_{timezone.now():%Y%m%d_%H%M}.xlsx"
    return build_excel_response(filename, "Biens", headers, _bien_rows(biens))



def export_services_csv(request):
    """Exporte la liste filtrée des services au format CSV."""
    services = _filtered_services(request)
    headers = ["Référence", "Catégorie", "Famille", "Désignation", "Fréquence", "Description"]
    filename = f"services_{timezone.now():%Y%m%d_%H%M}.csv"
    return build_csv_response(filename, headers, _service_rows(services))



def export_services_excel(request):
    """Exporte la liste filtrée des services au format Excel."""
    services = _filtered_services(request)
    headers = ["Référence", "Catégorie", "Famille", "Désignation", "Fréquence", "Description"]
    filename = f"services_{timezone.now():%Y%m%d_%H%M}.xlsx"
    return build_excel_response(filename, "Services", headers, _service_rows(services))
