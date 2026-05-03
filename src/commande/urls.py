from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = 'commande'
urlpatterns = [
    # Pages principales
    path('', index_commande, name='index-commande'),
    path('liste/', liste_commandes, name='liste-commandes'),
    
    # CRUD Commandes
    path('ajouter/', CreateUpdateView_commande, name='ajouter-commande'),
    path('modifier/<int:pk>/', CreateUpdateView_commande, name='modifier-commande'),
    path('detail/<int:pk>/', detail_commande, name='detail-commande'),
    path('supprimer/<int:pk>/', supprimer_commande, name='supprimer-commande'),
    
    # HTMX - Lignes de commande
    path('ligne/ajouter/', commande_ligne_add, name='commande-ligne-add'),
    path('ligne/supprimer/', commande_ligne_delete, name='commande-ligne-delete'),
    path('charger_items/', charger_items, name='charger-items'),

    #----------------------------------------------------------------------
    # LIVRAISONS
    #----------------------------------------------------------------------
    path('livraison/', index_livraison, name='index-livraison'),
    path('livraison/liste/', liste_livraisons, name='liste-livraisons'),
    path('livraison/ajouter/', CreateUpdateView_livraison, name='ajouter-livraison'),
    path('livraison/modifier/<int:pk>/', CreateUpdateView_livraison, name='modifier-livraison'),
    path('livraison/detail/<int:pk>/', detail_livraison, name='detail-livraison'),
    path('livraison/supprimer/<int:pk>/', supprimer_livraison, name='supprimer-livraison'),
    
]
