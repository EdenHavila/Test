
from django.urls import path
from .views import *


app_name='Demande'
urlpatterns = [
    path('index', index,name='index'),
    path('liste/', liste, name='liste-demandes'),
    path('export/csv/', export_demandes_csv, name='export-demandes-csv'),
    path('export/excel/', export_demandes_excel, name='export-demandes-excel'),
    path('ajouter/', CreateUpdateView, name='ajouter-demande'),
    path('modifier/<int:pk>/', CreateUpdateView, name='modifier-demande'),
    path('supprimer/<int:pk>/', supprimer_demande, name='supprimer-demande'),
    path('detail/<int:pk>/', detail_demande, name='detail-demande'),
    
    # Mes demandes (demandes de l'utilisateur connecté)
    path('mes-demandes/', mes_demandes_index, name='mes-demandes'),
    path('mes-demandes/liste/', mes_demandes_liste, name='mes-demandes-liste'),
    path('mes-demandes/export/csv/', export_mes_demandes_csv, name='mes-demandes-export-csv'),
    path('mes-demandes/export/excel/', export_mes_demandes_excel, name='mes-demandes-export-excel'),

    path("ligne-add/", ligne_add, name="ligne-add"),
    path("charge-champ-demandes-associes/",charge_champ_demandes, name="charge_champ_demandes"),

]
