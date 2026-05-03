
from django.urls import path
from .views import *


app_name='Demande'
urlpatterns = [
    path('index', index,name='index'),
    path('liste/', liste, name='liste-demandes'),
    path('ajouter/', CreateUpdateView, name='ajouter-demande'),
    path('modifier/<int:pk>/', CreateUpdateView, name='modifier-demande'),
    path('supprimer/<int:pk>/', supprimer_demande, name='supprimer-demande'),
    path('detail/<int:pk>/', detail_demande, name='detail-demande'),
    
    # Mes demandes (demandes de l'utilisateur connecté)
    path('mes-demandes/', mes_demandes_index, name='mes-demandes'),
    path('mes-demandes/liste/', mes_demandes_liste, name='mes-demandes-liste'),

    path("ligne-add/", ligne_add, name="ligne-add"),
    path("charge-champ-demandes-associes/",charge_champ_demandes, name="charge_champ_demandes"),

]
