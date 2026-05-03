from django.contrib import admin
from .models import  *
# Register your models here.


@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ['code_demande', 'type_demande', 'nature_demande', 'date_demande', 'statut_demande', 'motif_demande', 'demandes_associees_list']    
    search_fields = ('code_demande', 'motif_demande')
    filter_horizontal = ('demandes_associees',)  # widget pratique pour ManyToMany self

    def demandes_associees_list(self, obj):
        return ", ".join(d.code_demande for d in obj.demandes_associees.all())
    demandes_associees_list.short_description = 'Demandes associées'