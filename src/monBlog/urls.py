from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('ajouter/', ajouter_article,name='ajouter_article'),
    path('liste/', liste_articles, name='liste_articles'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('delete/<int:article_id>/', delete_article, name='delete_article'),
    path('modifier/<int:article_id>/', modifier_article, name='modifier_article'),
    path('contact/', contact_view, name='contact'),
]
