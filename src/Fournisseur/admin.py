from django.contrib import admin
from .models import  *
# Register your models here.


#admin.site.register(Fournisseur)

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['reference', 'nom', 'email', 'telephone', 'statut','types_list', 'specialite_list']
        # Méthode pour afficher les types (ManyToManyField)
    def types_list(self, obj):
        return ", ".join([str(t) for t in obj.types.all()])
    types_list.short_description = "Types"

    # Méthode pour afficher les spécialités (ManyToManyField)
    def specialite_list(self, obj):
        return ", ".join([str(s) for s in obj.specialite.all()])
    specialite_list.short_description = "Spécialités"

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['nom']