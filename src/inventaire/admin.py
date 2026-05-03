from django.contrib import admin
from django.utils.html import format_html
from .models import Stock, MouvementLogistique


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [
        'code', 
        'bien', 
        'lieu_stockage_display', 
        'quantite_display', 
        'unite', 
        'niveau_alerte', 
        'statut_display', 
        'responsable_stock', 
        'date_mise_a_jour'
    ]
    list_filter = ['lieu_stockage', 'statut_bien', 'unite']
    search_fields = ['code', 'bien__designation', 'responsable_stock__username']
    readonly_fields = ['code', 'date_mise_a_jour']
    raw_id_fields = ['bien', 'responsable_stock']
    list_per_page = 25
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'bien', 'lieu_stockage')
        }),
        ('Quantités', {
            'fields': ('quantite_disponible', 'unite', 'niveau_alerte')
        }),
        ('Statut et responsable', {
            'fields': ('statut_bien', 'responsable_stock', 'date_mise_a_jour')
        }),
    )
    
    @admin.display(description='Lieu de stockage')
    def lieu_stockage_display(self, obj):
        return obj.get_lieu_stockage_display()
    
    @admin.display(description='Quantité')
    def quantite_display(self, obj):
        if obj.alerte_stock:
            return format_html(
                '<span style="color: red; font-weight: bold;">⚠️ {}</span>',
                obj.quantite_disponible
            )
        return obj.quantite_disponible
    
    @admin.display(description='Statut')
    def statut_display(self, obj):
        if obj.statut_bien == 'disponible':
            return format_html('<span style="color: green;">✓ Disponible</span>')
        elif obj.statut_bien == 'indisponible':
            return format_html('<span style="color: red;">✗ Indisponible</span>')
        return '-'


@admin.register(MouvementLogistique)
class MouvementLogistiqueAdmin(admin.ModelAdmin):
    list_display = [
        'code', 
        'stock_display',
        'type_mouvement_display', 
        'quantite', 
        'source_display',
        'destination',
        'responsable', 
        'date_mouvement'
    ]
    list_filter = ['type_mouvement', 'source', 'destination_type', 'date_mouvement']
    search_fields = [
        'code', 
        'stock__code', 
        'stock__bien__designation', 
        'responsable__username',
        'destination'
    ]
    readonly_fields = ['code']
    raw_id_fields = ['stock', 'responsable']
    date_hierarchy = 'date_mouvement'
    list_per_page = 25
    
    fieldsets = (
        ('Informations du mouvement', {
            'fields': ('code', 'stock', 'type_mouvement', 'quantite', 'date_mouvement')
        }),
        ('Source et Destination', {
            'fields': ('source', 'destination_type', 'destination')
        }),
        ('Justification', {
            'fields': ('justification', 'reference_document')
        }),
        ('Responsable', {
            'fields': ('responsable',)
        }),
    )
    
    @admin.display(description='Stock')
    def stock_display(self, obj):
        return f"{obj.stock.code} - {obj.stock.bien.designation}"
    
    @admin.display(description='Type')
    def type_mouvement_display(self, obj):
        colors = {
            'ENT': 'green',
            'SOR': 'red',
            'TRF': 'blue',
            'RET': 'orange',
            'COR': 'purple',
        }
        color = colors.get(obj.type_mouvement, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_type_mouvement_display()
        )
    
    @admin.display(description='Source')
    def source_display(self, obj):
        return obj.get_source_display()
