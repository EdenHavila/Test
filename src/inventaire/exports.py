from django.utils import timezone
from monprojet.utils.export_utils import build_csv_response, build_excel_response
from .models import Stock, MouvementLogistique


def _filtered_stock(request):
    """Construit la liste filtrée des stocks."""
    stocks = Stock.objects.select_related('bien', 'bien__sous_categorie', 'responsable_stock').all().order_by('code')

    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        stocks = stocks.filter(
            Q(code__icontains=q) |
            Q(bien__designation__icontains=q)
        )

    lieu = request.GET.get('lieu', '').strip()
    if lieu:
        stocks = stocks.filter(lieu_stockage=lieu)

    statut = request.GET.get('statut', '').strip()
    if statut:
        stocks = stocks.filter(statut_bien=statut)

    unite = request.GET.get('unite', '').strip()
    if unite:
        stocks = stocks.filter(unite=unite)

    date_debut = request.GET.get('date_debut', '').strip()
    if date_debut:
        stocks = stocks.filter(date_mise_a_jour__date__gte=date_debut)

    date_fin = request.GET.get('date_fin', '').strip()
    if date_fin:
        stocks = stocks.filter(date_mise_a_jour__date__lte=date_fin)

    return stocks



def _filtered_mouvements(request):
    """Construit la liste filtrée des mouvements logistiques."""
    mouvements = MouvementLogistique.objects.select_related('stock', 'stock__bien', 'responsable').all().order_by('-date_mouvement')

    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        mouvements = mouvements.filter(
            Q(code__icontains=q) |
            Q(stock__bien__designation__icontains=q) |
            Q(destination__icontains=q) |
            Q(destination_type__icontains=q)
        )

    type_mouvement = request.GET.get('type_mouvement', '').strip()
    if type_mouvement:
        mouvements = mouvements.filter(type_mouvement=type_mouvement)

    source = request.GET.get('source', '').strip()
    if source:
        mouvements = mouvements.filter(source=source)

    date_debut = request.GET.get('date_debut', '').strip()
    if date_debut:
        mouvements = mouvements.filter(date_mouvement__date__gte=date_debut)

    date_fin = request.GET.get('date_fin', '').strip()
    if date_fin:
        mouvements = mouvements.filter(date_mouvement__date__lte=date_fin)

    return mouvements



def _stock_rows(stocks):
    """Prépare les lignes d'export pour les stocks."""
    return [
        [
            stock.code,
            stock.bien.designation if stock.bien else '-',
            stock.bien.sous_categorie.nom if stock.bien and stock.bien.sous_categorie else '-',
            stock.get_lieu_stockage_display() if hasattr(stock, 'get_lieu_stockage_display') else stock.lieu_stockage,
            stock.quantite_disponible,
            stock.get_unite_display() if hasattr(stock, 'get_unite_display') else stock.unite,
            stock.get_statut_bien_display() if hasattr(stock, 'get_statut_bien_display') else stock.statut_bien,
            stock.responsable_stock.get_username() if stock.responsable_stock else '-',
            stock.date_mise_a_jour.strftime('%d/%m/%Y %H:%M') if stock.date_mise_a_jour else '-',
            stock.niveau_alerte,
        ]
        for stock in stocks
    ]



def _mouvement_rows(mouvements):
    """Prépare les lignes d'export pour les mouvements logistiques."""
    return [
        [
            mouvement.code,
            mouvement.date_mouvement.strftime('%d/%m/%Y %H:%M') if mouvement.date_mouvement else '-',
            mouvement.get_type_mouvement_display() if hasattr(mouvement, 'get_type_mouvement_display') else mouvement.type_mouvement,
            mouvement.quantite,
            mouvement.get_source_display() if hasattr(mouvement, 'get_source_display') else mouvement.source,
            mouvement.get_destination_type_display() if hasattr(mouvement, 'get_destination_type_display') else mouvement.destination_type,
            mouvement.destination or '-',
            mouvement.responsable.get_username() if mouvement.responsable else '-',
            mouvement.stock.code if mouvement.stock else '-',
            mouvement.justification or '-',
        ]
        for mouvement in mouvements
    ]



def export_stock_csv(request):
    """Exporte la liste filtrée des stocks au format CSV."""
    stocks = _filtered_stock(request)
    headers = ["Code", "Bien", "Sous-catégorie", "Lieu", "Quantité", "Unité", "Statut", "Responsable", "Mise à jour", "Seuil"]
    filename = f"stocks_{timezone.now():%Y%m%d_%H%M}.csv"
    return build_csv_response(filename, headers, _stock_rows(stocks))



def export_stock_excel(request):
    """Exporte la liste filtrée des stocks au format Excel."""
    stocks = _filtered_stock(request)
    headers = ["Code", "Bien", "Sous-catégorie", "Lieu", "Quantité", "Unité", "Statut", "Responsable", "Mise à jour", "Seuil"]
    filename = f"stocks_{timezone.now():%Y%m%d_%H%M}.xlsx"
    return build_excel_response(filename, "Stocks", headers, _stock_rows(stocks))



def export_mouvements_csv(request):
    """Exporte la liste filtrée des mouvements au format CSV."""
    mouvements = _filtered_mouvements(request)
    headers = ["Code", "Date", "Type", "Quantité", "Source", "Destination type", "Destination", "Responsable", "Stock", "Justification"]
    filename = f"mouvements_{timezone.now():%Y%m%d_%H%M}.csv"
    return build_csv_response(filename, headers, _mouvement_rows(mouvements))



def export_mouvements_excel(request):
    """Exporte la liste filtrée des mouvements au format Excel."""
    mouvements = _filtered_mouvements(request)
    headers = ["Code", "Date", "Type", "Quantité", "Source", "Destination type", "Destination", "Responsable", "Stock", "Justification"]
    filename = f"mouvements_{timezone.now():%Y%m%d_%H%M}.xlsx"
    return build_excel_response(filename, "Mouvements", headers, _mouvement_rows(mouvements))
