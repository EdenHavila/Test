from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalogue.urls import app_name
from .views import *

app_name='Fournisseur'
urlpatterns = [
    path('index', index,name='index'),
    path("specialite/", charger_specialite, name="charger_specialite"),

    #path('get_biens_or_services/', get_biens_or_services, name='get-biens-or-services'),


    path('ajouter_fournisseur/', CreateUpdateView,name='ajouter-fournisseur'),
    path('modifier_fournisseur/<int:pk>/', CreateUpdateView, name='modifier-fournisseur'),
    path('liste/', liste_fournisseurs, name='liste-fournisseurs'),
    path('detail/<int:pk>/', detail_fournisseur, name='detail-fournisseur'),
    path('delete/<int:pk>/', supprimer_fournisseur, name='delete'),

]
