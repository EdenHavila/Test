from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *

# Create your views here.
def index(request):
    return render(request,'monBlog/index.html')

def ajouter_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_articles')
            # Redirige vers la liste des articles (à définir)
    else:
        form = ArticleForm()

    return render(request, 'monBlog/ajouter_article.html', {'form': form})


def liste_articles(request):
    articles = Article.objects.all()  # Récupérer tous les articles
    return render(request, 'monBlog/liste_articles.html', {'articles': articles})




def article_detail(request, article_id):
    # Récupère l'article avec l'ID fourni ou retourne une erreur 404 si non trouvé
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'monBlog/article_detail.html', {'article': article})



def delete_article(request, article_id):
    # Récupère l'article avec l'ID fourni ou retourne une erreur 404 si non trouvé
    article = get_object_or_404(Article, pk=article_id)
    if request.method=="POST":
        article.delete()
        messages.success(request, 'L\'objet a bien été supprimé.')
        return redirect('liste_articles')
    return render(request, 'monBlog/confirmation_suppression.html', {'article': article})




def modifier_article(request,article_id,*args, **kwargs):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST,request.FILES,instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', article_id= article.id) # Rediriger vers la page de l'article modifié

    else:
        form = ArticleForm( instance=article)

    return render(request, 'monBlog/ajouter_article.html', {'form': form})















def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistre les données dans la base de données
             # Redirige vers une page de succès après la soumission
    else:
        form = ContactForm()

    return render(request, 'monBLog/contact_form.html', {'form': form})