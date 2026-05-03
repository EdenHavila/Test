from django.contrib import admin
from .models import  *
# Register your models here.


#admin.site.register(Bien)
#admin.site.register(Categorie)
admin.site.register(Service)


@admin.register(Famille)
class FamilleAdmin(admin.ModelAdmin):
    list_display = ['reference','designation']

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['reference', 'designation','famille']

@admin.register(SousCategorie)
class SousCategorieAdmin(admin.ModelAdmin):
    list_display = ['reference','type', 'nom']

@admin.register(Bien)
class BienAdmin(admin.ModelAdmin):
    list_display = ['reference','designation', 'frequence_utilisation','sous_categorie']
