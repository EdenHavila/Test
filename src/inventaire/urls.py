from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalogue.urls import app_name
from .views import *
from .exports import *

app_name='inventaire'
urlpatterns = [
    path('index_stock', index_stock,name='index-stock'),
    path('ajouter_stock/', CreateUpdateView_stock,name='ajouter-stock'),
    path('modifier_stock/<int:pk>/', CreateUpdateView_stock, name='modifier-stock'),
    path('liste_stock/', liste_stock, name='liste-stock'),
    path('export/stock/csv/', export_stock_csv, name='export-stock-csv'),
    path('export/stock/excel/', export_stock_excel, name='export-stock-excel'),
    path('detail_stock/<int:pk>/', detail_stock, name='detail-stock'),
    path('delete/<int:pk>/', supprimer_stock, name='delete-stock'),


    path('index_mouvement', index_mouvement,name='index-mouvement'),
    path('ajouter_mouvement/', CreateUpdateView_mouvement,name='ajouter-mouvement'),
    path('modifier_mouvement/<int:pk>/', CreateUpdateView_mouvement, name='modifier-mouvement'),
    path('liste_mouvement/', liste_mouvement, name='liste-mouvement'),
    path('export/mouvement/csv/', export_mouvements_csv, name='export-mouvements-csv'),
    path('export/mouvement/excel/', export_mouvements_excel, name='export-mouvements-excel'),
    path('detail_mouvement/<int:pk>/', detail_mouvement, name='detail-mouvement'),
    path('delete_mouvement/<int:pk>/', supprimer_mouvement, name='delete-mouvement'),
]
