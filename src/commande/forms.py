from django import forms
from django.forms import inlineformset_factory
from django.db.models import Q
from .models import Commande, LigneCommande
from Demande.models import Demande
from Fournisseur.models import Fournisseur
from catalogue.models import Bien, Service
from django_select2.forms import Select2Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class CommandeForm(forms.ModelForm):
    demande = forms.ModelChoiceField(
        queryset=Demande.objects.filter(
            type_demande='Gestionnaire'
        ).order_by('-date_demande'),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Demande associée",
        empty_label="-- Sélectionner une demande --"
    )
    
    fournisseur = forms.ModelChoiceField(
        queryset=Fournisseur.objects.filter(statut='Actif'),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Fournisseur",
        empty_label="-- Sélectionner un fournisseur --"
    )

    class Meta:
        model = Commande
        fields = ['demande', 'fournisseur', 'date_cmnd', 'statut_cmnd', 'fichier_bon_cmnd']
        widgets = {
            'date_cmnd': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'statut_cmnd': forms.Select(attrs={'class': 'form-select'}),
            'fichier_bon_cmnd': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'date_cmnd': 'Date de commande',
            'statut_cmnd': 'Statut',
            'fichier_bon_cmnd': 'Bon de commande',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # On gère la balise form dans le template
        self.helper.layout = Layout(
            Row(
                Column('demande', css_class='col-md-6'),
                Column('fournisseur', css_class='col-md-6'),
                css_class='mb-3'
            ),
            Row(
                Column('date_cmnd', css_class='col-md-4'),
                Column('statut_cmnd', css_class='col-md-4'),
                Column('fichier_bon_cmnd', css_class='col-md-4'),
                css_class='mb-3'
            ),
        )
        # Lors de l'édition, conserver le fournisseur courant même s'il est devenu inactif,
        # sinon n'afficher que les fournisseurs actifs pour la sélection.
        if self.instance and getattr(self.instance, 'fournisseur', None):
            current = self.instance.fournisseur
            if current and current.statut != 'Actif':
                self.fields['fournisseur'].queryset = Fournisseur.objects.filter(
                    Q(pk=current.pk) | Q(statut='Actif')
                )


class LigneCommandeForm(forms.ModelForm):
    """Formulaire pour une ligne de commande individuelle"""
    
    class Meta:
        model = LigneCommande
        fields = ['type', 'bien', 'service', 'quantite', 'prix_unitaire']
        labels = {
            'type': 'Type',
            'bien': 'Bien',
            'service': 'Service',
            'quantite': 'Quantité',
            'prix_unitaire': 'Prix unitaire',
        }
        widgets = {
            'quantite': forms.NumberInput(attrs={'min': '1'}),
            'prix_unitaire': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialiser les querysets
        self.fields['bien'].queryset = Bien.objects.all()
        self.fields['service'].queryset = Service.objects.all()
        self.fields['bien'].required = False
        self.fields['service'].required = False
        self.fields['quantite'].initial = 1
        self.fields['prix_unitaire'].required = False

    def clean(self):
        cleaned_data = super().clean()
        type_item = cleaned_data.get('type')
        bien = cleaned_data.get('bien')
        service = cleaned_data.get('service')

        if type_item == 'Bien' and not bien:
            self.add_error('bien', 'Veuillez sélectionner un bien.')
        elif type_item == 'Service' and not service:
            self.add_error('service', 'Veuillez sélectionner un service.')

        return cleaned_data


# InlineFormSet pour gérer plusieurs lignes de commande
LigneCommandeFormSet = inlineformset_factory(
    Commande,
    LigneCommande,
    form=LigneCommandeForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


# =============================================================================
# FORMULAIRES LIVRAISON
# =============================================================================
from .models import Livraison


class LivraisonForm(forms.ModelForm):
    """Formulaire pour créer ou modifier une livraison"""
    
    commande = forms.ModelChoiceField(
        queryset=Commande.objects.all().order_by('-date_cmnd'),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Commande associée",
        empty_label="-- Sélectionner une commande --"
    )

    class Meta:
        model = Livraison
        fields = ['commande', 'date_livraison', 'statut', 'fichier_bon_livraison', 'observation']
        widgets = {
            'date_livraison': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'fichier_bon_livraison': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observations...'}),
        }
        labels = {
            'date_livraison': 'Date de livraison',
            'statut': 'Statut',
            'fichier_bon_livraison': 'Bon de livraison',
            'observation': 'Observations',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('commande', css_class='col-md-6'),
                Column('date_livraison', css_class='col-md-6'),
                css_class='mb-3'
            ),
            Row(
                Column('statut', css_class='col-md-6'),
                Column('fichier_bon_livraison', css_class='col-md-6'),
                css_class='mb-3'
            ),
            Row(
                Column('observation', css_class='col-12'),
                css_class='mb-3'
            ),
        )