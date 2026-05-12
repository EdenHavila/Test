from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from .exports import *

app_name = 'catalogue'
urlpatterns = [
    # Bien
    path('index/', index_bien, name='index-bien'),
    path('bien/ajouter/', CreateUpdateBienView, name='ajouter-bien'),
    path('bien/modifier/<int:pk>/', CreateUpdateBienView, name='modifier-bien'),
    path('bien/detail/<int:pk>/', detail_bien, name='detail-bien'),
    path('bien/delete/<int:pk>/', supprimer_bien, name='delete-bien'),
    path('bien/liste/', liste_biens, name='liste-biens'),
    path('bien/export/csv/', export_biens_csv, name='export-biens-csv'),
    path('bien/export/excel/', export_biens_excel, name='export-biens-excel'),

    # Service
    path('service/index/', index_service, name='index-service'),
    path('service/liste/', liste_services, name='liste-services'),
    path('service/export/csv/', export_services_csv, name='export-services-csv'),
    path('service/export/excel/', export_services_excel, name='export-services-excel'),
    path('service/ajouter/', CreateUpdateServiceView, name='ajouter-service'),
    path('service/modifier/<int:pk>/', CreateUpdateServiceView, name='modifier-service'),
    path('service/detail/<int:pk>/', detail_service, name='detail-service'),
    # Pour la suite, prévoir delete_service

    # Liste mixte
    path('liste/', liste_biens_services, name='liste-biens-services'),

    ###path('liste/', liste_articles, name='liste_articles'),
    ###path('article/<int:article_id>/', article_detail, name='article_detail'),
    ###path('delete/<int:article_id>/', delete_article, name='delete_article'),
    ###path('modifier/<int:article_id>/', modifier_article, name='modifier_article'),
    ###path('contact/', contact_view, name='contact'),
]
