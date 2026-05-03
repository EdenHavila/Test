from django import forms
from .models import Stock, MouvementLogistique
from accounts.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Div, HTML, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['bien', 'lieu_stockage', 'quantite_disponible', 'unite', 'niveau_alerte', 'statut_bien', 'responsable_stock', 'date_mise_a_jour']
        widgets = {
            'date_mise_a_jour': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrer les utilisateurs pour n'afficher que les gestionnaires
        self.fields['responsable_stock'].queryset = User.objects.filter(
            role__nom_role='gestionnaire'
        )
        # Personnaliser l'affichage des utilisateurs dans le select
        self.fields['responsable_stock'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name} ({obj.username})"
        
        # Configuration Crispy Forms
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # Section Article
            HTML('<div class="form-section"><h6 class="form-section-title"><i class="bi bi-box-seam me-2"></i>Article</h6></div>'),
            Row(
                Column('bien', css_class='col-md-12 mb-3'),
                css_class='row'
            ),
            
            # Section Stockage
            HTML('<div class="form-section"><h6 class="form-section-title"><i class="bi bi-geo-alt me-2"></i>Stockage</h6></div>'),
            Row(
                Column('lieu_stockage', css_class='col-md-6 mb-3'),
                Column('statut_bien', css_class='col-md-6 mb-3'),
                css_class='row'
            ),
            
            # Section Quantités
            HTML('<div class="form-section"><h6 class="form-section-title"><i class="bi bi-123 me-2"></i>Quantités</h6></div>'),
            Row(
                Column('quantite_disponible', css_class='col-md-4 mb-3'),
                Column('unite', css_class='col-md-4 mb-3'),
                Column('niveau_alerte', css_class='col-md-4 mb-3'),
                css_class='row'
            ),
            
            # Section Responsable
            HTML('<div class="form-section"><h6 class="form-section-title"><i class="bi bi-person-check me-2"></i>Responsable & Date</h6></div>'),
            Row(
                Column('responsable_stock', css_class='col-md-6 mb-3'),
                Column('date_mise_a_jour', css_class='col-md-6 mb-3'),
                css_class='row'
            ),
        )

    def clean_responsable_stock(self):
        """Valide que le responsable sélectionné a bien le rôle gestionnaire."""
        responsable = self.cleaned_data.get('responsable_stock')
        
        if responsable:
            if not responsable.role:
                raise forms.ValidationError(
                    "Cet utilisateur n'a pas de rôle assigné."
                )
            if responsable.role.nom_role != 'gestionnaire':
                raise forms.ValidationError(
                    "Le responsable du stock doit avoir le rôle 'gestionnaire'."
                )
        
        return responsable


class MouvementLogistiqueForm(forms.ModelForm):
    class Meta:
        model = MouvementLogistique
        fields = [
            'stock', 
            'type_mouvement', 
            'quantite', 
            'source', 
            'destination_type', 
            'destination', 
            'justification', 
            'reference_document', 
            'responsable', 
            'date_mouvement'
        ]
        widgets = {
            'date_mouvement': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'justification': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Motif du mouvement...'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir l'utilisateur connecté comme responsable par défaut
        if user:
            self.fields['responsable'].initial = user
            self.fields['responsable'].disabled = True
        
        # Filtrer les responsables (gestionnaires uniquement)
        self.fields['responsable'].queryset = User.objects.filter(
            role__nom_role='gestionnaire'
        )
        self.fields['responsable'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"
        
        # Personnaliser l'affichage du stock dans le select
        self.fields['stock'].label_from_instance = lambda obj: f"{obj.code} - {obj.bien.designation} ({obj.get_lieu_stockage_display()})"
        
        # Rendre certains champs optionnels
        self.fields['justification'].required = False
        self.fields['reference_document'].required = False
        self.fields['destination'].required = False
        
        # Configuration Crispy Forms
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # Section Stock concerné
            HTML('<div class="form-section"><h6 class="form-section-title"><i class="bi bi-box me-2"></i>Stock concerné</h6></div>'),
            Row(
                Column('stock', css_class='col-md-12 mb-3'),
                css_class='row'
            ),
            
            # Section Type de mouvement
            HTML('<div class="form-section"><h6 class="form-section-title"><i class="bi bi-arrow-left-right me-2"></i>Type & Quantité</h6></div>'),
            Row(
                Column('type_mouvement', css_class='col-md-6 mb-3'),
                Column('quantite', css_class='col-md-6 mb-3'),
                css_class='row'
            ),
            
            # Section Source et Destination
            HTML('<div class="form-section"><h6 class="form-section-title"><i class="bi bi-signpost-split me-2"></i>Source & Destination</h6></div>'),
            Row(
                Column('source', css_class='col-md-4 mb-3'),
                Column('destination_type', css_class='col-md-4 mb-3'),
                Column('destination', css_class='col-md-4 mb-3'),
                css_class='row'
            ),
            
            # Section Justification
            HTML('<div class="form-section"><h6 class="form-section-title"><i class="bi bi-card-text me-2"></i>Justification</h6></div>'),
            Row(
                Column('justification', css_class='col-md-12 mb-3'),
                css_class='row'
            ),
            Row(
                Column('reference_document', css_class='col-md-12 mb-3'),
                css_class='row'
            ),
            
            # Section Responsable
            HTML('<div class="form-section"><h6 class="form-section-title"><i class="bi bi-person-badge me-2"></i>Responsable & Date</h6></div>'),
            Row(
                Column('responsable', css_class='col-md-6 mb-3'),
                Column('date_mouvement', css_class='col-md-6 mb-3'),
                css_class='row'
            ),
        )

    def clean(self):
        """Validation globale du formulaire."""
        cleaned_data = super().clean()
        stock = cleaned_data.get('stock')
        quantite = cleaned_data.get('quantite')
        type_mouvement = cleaned_data.get('type_mouvement')
        
        if stock and quantite and type_mouvement:
            # Vérifier le stock disponible pour les sorties et transferts
            if type_mouvement in ['SOR', 'TRF']:
                if quantite > stock.quantite_disponible:
                    self.add_error(
                        'quantite', 
                        f"Stock insuffisant. Quantité disponible : {stock.quantite_disponible}"
                    )
        
        return cleaned_data

    def clean_quantite(self):
        """Validation de la quantité."""
        quantite = self.cleaned_data.get('quantite')
        if quantite is not None and quantite <= 0:
            raise forms.ValidationError("La quantité doit être supérieure à 0.")
        return quantite