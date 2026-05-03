from django import forms
from .models import Demande,DetailsDemande
from catalogue.models import Bien,Service
from django_select2.forms import Select2MultipleWidget
from django.forms import inlineformset_factory
# Formset pour gérer dynamiquement les lignes de détails de demande
FormSetDetailsDemande = inlineformset_factory(
    Demande,
    DetailsDemande,
    fields=['type', 'bien', 'service', 'quantite'],  # motif retiré
    extra=1,
    can_delete=True
)




"""
class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['type_demande','date', 'fichier_joint']
        widgets = {
            'type_demande': forms.Select(attrs={'class': 'form-select', }),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'fichier_joint': forms.ClearableFileInput(attrs={'class': 'form-control'}),


        }
"""


"""

"""




class DemandeForm(forms.ModelForm):

    class Meta:
        model = Demande
        fields = ['type_demande', 'nature_demande', 'date_demande', 'demandes_associees', 'motif_demande', 'statut_demande', 'fichier_joint']
        widgets = {
            'date_demande': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'motif_demande': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Motif de la demande...'}),
            'demandes_associees': Select2MultipleWidget(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Sélectionnez les demandes à regrouper',
                'style': 'min-height: 44px; font-size: 1rem;'
            }),
            'statut_demande': forms.Select(attrs={'class': 'form-select'}),
            'fichier_joint': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Sécurité : si pas d'utilisateur, retirer les champs sensibles
        if not user:
            self.fields.pop("demandes_associees", None)
            self.fields.pop("statut_demande", None)
            return

        # Déterminer les rôles de l'utilisateur
        is_demandeur = user.groups.filter(name="Demandeur").exists()
        is_gestionnaire = user.groups.filter(name="Gestionnaire").exists()

        # =============================================
        # RÈGLE 1 : Utilisateur DEMANDEUR (pas gestionnaire)
        # - type_demande = "Demandeur" (fixé et grisé)
        # - demandes_associees = CACHÉ
        # - statut_demande = CACHÉ
        # =============================================
        if is_demandeur and not is_gestionnaire:
            self.fields["type_demande"].initial = "Demandeur"
            self.fields["type_demande"].disabled = True
            self.fields.pop("statut_demande", None)
            self.fields.pop("demandes_associees", None)
            return

        # =============================================
        # RÈGLE 2 : Utilisateur GESTIONNAIRE
        # - type_demande = choix libre
        # - statut_demande = VISIBLE (pour changer le statut)
        # - demandes_associees = VISIBLE seulement si type_demande == "Gestionnaire"
        # =============================================
        if is_gestionnaire:
            # Déterminer la valeur actuelle de type_demande
            type_d = None
            
            # Priorité 1 : instance existante (édition)
            if self.instance and getattr(self.instance, 'pk', None):
                type_d = self.instance.type_demande
            
            # Priorité 2 : données soumises (POST/GET via HTMX)
            if not type_d and self.data:
                if hasattr(self.data, 'getlist'):
                    type_list = self.data.getlist('type_demande')
                    type_d = type_list[-1] if type_list else None
                else:
                    type_d = self.data.get('type_demande')
            
            # Normaliser et comparer
            type_d_norm = (type_d or "").strip().lower()
            
            if type_d_norm == "gestionnaire":
                # Afficher le champ avec seulement les demandes de type Demandeur
                # Exclure la demande actuelle si on est en édition
                qs = Demande.objects.filter(type_demande="Demandeur").order_by("-pk")
                self.fields["demandes_associees"].queryset = qs
                
                # Pré-remplir avec les demandes déjà associées en mode édition
                if self.instance and self.instance.pk:
                    self.fields["demandes_associees"].initial = self.instance.demandes_associees.all()
            else:
                # Masquer le champ
                self.fields.pop("demandes_associees", None)
            return

        # =============================================
        # RÈGLE 3 : Autre cas (ni demandeur, ni gestionnaire)
        # - demandes_associees = CACHÉ
        # - statut_demande = CACHÉ
        # =============================================
        self.fields.pop("demandes_associees", None)
        self.fields.pop("statut_demande", None)

