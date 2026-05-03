from django import forms
from .models import Fournisseur, Type
from catalogue.models import SousCategorie
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML


class FournisseurForm(forms.ModelForm):
    types = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        to_field_name='nom',
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label="Type de fournisseur"
    )
    specialite = forms.ModelMultipleChoiceField(
        queryset=SousCategorie.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True,
        label="Spécialités"
    )

    class Meta:
        model = Fournisseur
        fields = ['nom', 'email', 'telephone', 'adresse', 'types', 'specialite']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du fournisseur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemple.com'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+225 XX XX XX XX'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse complète'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        type_names = []

        key = self.add_prefix('types')
        # Si le formulaire est soumis (POST), récupérer les noms envoyés
        if self.is_bound:
            raw_list = []
            if hasattr(self.data, 'getlist'):
                raw_list = self.data.getlist(key)
            else:
                raw = self.data.get(key) or []
                if isinstance(raw, str):
                    raw_list = [v for v in raw.split(',') if v]
                else:
                    raw_list = list(raw)
            if raw_list:
                type_names = [str(v) for v in raw_list if v]
            elif getattr(self.instance, 'pk', None):
                type_names = list(self.instance.types.values_list('nom', flat=True))
        elif getattr(self.instance, 'pk', None):
            type_names = list(self.instance.types.values_list('nom', flat=True))

        self.fields['specialite'].queryset = SousCategorie.objects.filter(type__in=type_names)