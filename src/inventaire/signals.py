#un signal automatique Django pour mettre à jour le stock dès qu’un mouvement logistique est enregistré
# Cela garantit que le stock est toujours synchronisé sans intervention manuelle.
# Il écoute les événements de création et de mise à jour des mouvements logistiques


#*👉 Le fichier signals.py appelle la logique métier (dans services.py) lorsqu’un événement survient.

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MouvementLogistique
from .services import enregistrer_mouvement, StockInsuffisantError
import logging



# Configuration du logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=MouvementLogistique)
def mise_a_jour_stock(sender, instance, created, **kwargs):
    """Signal pour mettre à jour automatiquement le stock après un mouvement."""
    if created:  # Éviter de recalculer si c'est juste une mise à jour
        try:
            resultat = enregistrer_mouvement(
                stock=instance.stock,
                quantite=instance.quantite,
                type_mouvement=instance.type_mouvement
            )
            
            logger.info(
                f"Stock {instance.stock.code} mis à jour après mouvement {instance.code}. "
                f"Type: {instance.type_mouvement}, Quantité: {instance.quantite}"
            )
            
            # Vérifier si le seuil d'alerte est atteint
            if resultat.get('alerte'):
                logger.warning(resultat.get('message_alerte'))
                # Stocker l'alerte dans l'instance pour récupération dans la vue
                instance._alerte_stock = resultat.get('message_alerte')
                
        except StockInsuffisantError as e:
            # Log de l'erreur si stock insuffisant
            logger.error(f"Erreur de stock insuffisant: {e}")
            # Supprimer le mouvement invalide
            instance.delete()
            raise
        except Exception as e:
            # Log pour toute autre exception
            logger.exception(f"Erreur lors de la mise à jour du stock: {e}")
            raise
