#*une fonction metier:est une fonction qui gère les règles métier spécifiques à ton application.
#_C’est le cœur du fonctionnement fonctionnel de ton projet :
#_Elle répond à la question "Que doit faire l’application selon les règles du métier ?".

from .models import Stock
from django.db import transaction
from django.utils import timezone


# Exception personnalisée pour une gestion d'erreur spécifique
class StockInsuffisantError(Exception):
    pass


def enregistrer_mouvement(stock, quantite, type_mouvement):
    """
    Met à jour la quantité disponible du stock en fonction du type de mouvement.
    
    Args:
        stock: Instance du modèle Stock à mettre à jour
        quantite: Quantité à ajouter ou retirer
        type_mouvement: Type de mouvement (ENT, SOR, TRF, RET, COR)
    """
    # Utiliser une transaction atomique pour garantir la cohérence des données
    with transaction.atomic():
        # Recharger le stock avec un verrou pour éviter les conflits
        stock = Stock.objects.select_for_update().get(pk=stock.pk)
        
        if type_mouvement == 'ENT':  # Entrée
            stock.quantite_disponible += quantite
        elif type_mouvement == 'SOR':  # Sortie
            if stock.quantite_disponible >= quantite:
                stock.quantite_disponible -= quantite
            else:
                raise StockInsuffisantError(
                    f"Stock insuffisant pour {stock.bien}. "
                    f"Quantité disponible: {stock.quantite_disponible}, "
                    f"Quantité demandée: {quantite}"
                )
        elif type_mouvement == 'RET':  # Retour (ajoute au stock)
            stock.quantite_disponible += quantite
        elif type_mouvement == 'COR':  # Correction (remplace la valeur)
            stock.quantite_disponible = quantite
        elif type_mouvement == 'TRF':  # Transfert
            if stock.quantite_disponible >= quantite:
                stock.quantite_disponible -= quantite
            else:
                raise StockInsuffisantError(
                    f"Stock insuffisant pour le transfert de {stock.bien}. "
                    f"Quantité disponible: {stock.quantite_disponible}, "
                    f"Quantité demandée: {quantite}"
                )
        
        # Mettre à jour la date de mise à jour
        stock.date_mise_a_jour = timezone.now()
        
        # Mettre à jour le statut selon la quantité
        if stock.quantite_disponible == 0:
            stock.statut_bien = 'indisponible'
        else:
            stock.statut_bien = 'disponible'
        
        stock.save()
        
        # Vérifier si le seuil d'alerte est atteint et retourner le résultat
        return {
            'stock': stock,
            'alerte': stock.alerte_stock,
            'message_alerte': (
                f"⚠️ ALERTE STOCK : {stock.bien.designation} ({stock.code}) - "
                f"Quantité: {stock.quantite_disponible} ≤ Seuil: {stock.niveau_alerte}"
            ) if stock.alerte_stock else None
        }
