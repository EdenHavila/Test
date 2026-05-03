# monapplication/forms.py
from django import forms
from .models import Contact,Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu','image','attachment','status']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Veuillez saisir le titre svp!!', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['nom', 'email', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Votre nom', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Votre email', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Votre message', 'class': 'form-control'}),
        }