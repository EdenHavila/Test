from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required

"""
@login_required  # redirige vers la page de connexion si non connecté
def index(request):
    return render(request,'base.html')
"""

def messages_partial(request):
    storage = get_messages(request)
    return render(request, "messages.html",{"messages": storage})

# Rediriger la racine vers la page de connexion
def home(request):
    return redirect('accounts')  # 'login' doit être le nom de la vue de connexion


# redirige vers la page de connexion si non connecté
def index(request):
    return redirect('accounts:connexion')

