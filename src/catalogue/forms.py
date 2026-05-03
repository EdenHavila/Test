from django import forms
from .models import Bien, Service, Categorie, SousCategorie
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Fieldset, Submit, HTML


class BienForm(forms.ModelForm):
    """Formulaire pour créer ou modifier un bien"""
    
    sous_categorie = forms.ModelChoiceField(
        queryset=SousCategorie.objects.filter(type='Bien'),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Sous-catégorie",
        empty_label="-- Sélectionner une sous-catégorie --"
    )

    class Meta:
        model = Bien
        fields = ['sous_categorie', 'designation', 'frequence_utilisation', 'marque', 'modele', 'informations_complementaires']
        widgets = {
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la désignation du bien'
            }),
            'frequence_utilisation': forms.Select(attrs={
                'class': 'form-select'
            }),
            'marque': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marque du bien'
            }),
            'modele': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modèle du bien'
            }),
            'informations_complementaires': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Couleur, dimensions, spécifications, etc.'
            }),
        }
        labels = {
            'designation': 'Désignation',
            'frequence_utilisation': 'Fréquence d\'utilisation',
            'marque': 'Marque',
            'modele': 'Modèle',
            'informations_complementaires': 'Informations complémentaires',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # On gère la balise form dans le template
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(
                    Column('sous_categorie', css_class='col-md-6'),
                    Column('frequence_utilisation', css_class='col-md-6'),
                    css_class='mb-3'
                ),
                Row(
                    Column('designation', css_class='col-12'),
                    css_class='mb-3'
                ),
                Row(
                    Column('marque', css_class='col-md-6'),
                    Column('modele', css_class='col-md-6'),
                    css_class='mb-3'
                ),
                Row(
                    Column('informations_complementaires', css_class='col-12'),
                    css_class='mb-3'
                ),
            ),
        )


class ServiceForm(forms.ModelForm):
    """Formulaire pour créer ou modifier un service"""
    
    sous_categorie = forms.ModelChoiceField(
        queryset=SousCategorie.objects.filter(type='Service'),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Sous-catégorie",
        empty_label="-- Sélectionner une sous-catégorie --"
    )

    class Meta:
        model = Service
        fields = ['sous_categorie', 'designation', 'frequence', 'description']
        widgets = {
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la désignation du service'
            }),
            'frequence': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du service...'
            }),
        }
        labels = {
            'designation': 'Désignation',
            'frequence': 'Fréquence',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(
                    Column('sous_categorie', css_class='col-md-6'),
                    Column('frequence', css_class='col-md-6'),
                    css_class='mb-3'
                ),
                Row(
                    Column('designation', css_class='col-12'),
                    css_class='mb-3'
                ),
                Row(
                    Column('description', css_class='col-12'),
                    css_class='mb-3'
                ),
            ),
        )

