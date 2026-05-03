from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse email")

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

        labels = {
            'username': "Nom d'utilisateur",
            'first_name': "Prénom",
            'last_name': "Nom",
            'password1': "Mot de passe",
            'password2': "Confirmer le mot de passe",
        }



class ConnexionForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur ")
    password = forms.CharField(widget=forms.PasswordInput)