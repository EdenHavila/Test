from django.apps import AppConfig

# Configuration de l'application Inventaire
class InventaireConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventaire'

    def ready(self):
        # Importer les signaux pour les enregistrer
        import inventaire.signals

 
 

#Les signaux Django doivent être importés au démarrage de l'application pour être enregistrés. Sans la méthode 
#ready, les signaux ne seraient pas connectés, et les actions automatiques (comme la mise à jour du stock) ne fonctionneraient pas.
       