from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required



#import hmac
#import hashlib
#import os
#from django.http import HttpResponse
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







#GITHUB_SECRET = b"mysecret123" # Remplacez par votre propre secret, doit être en bytes (Le b devant "mysecret123" sert à dire à Python : "Traite cette chaîne de caractères comme des bytes")

"""
def verify_signature(request):
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        return False

    mac = hmac.new(
        GITHUB_SECRET,
        msg=request.body,
        digestmod=hashlib.sha256
    )

    expected = "sha256=" + mac.hexdigest()

    return hmac.compare_digest(signature, expected)


def github_webhook(request):
    if request.method != "POST":
        return HttpResponse("Only POST", status=405)

    if not verify_signature(request):
        return HttpResponse("Forbidden", status=403)

    os.system("/var/www/StaticsFiles/Test/deploy_test.sh") # Remplacez par le chemin vers votre script de déploiement

    return HttpResponse("OK")
"""
