from django.urls import path
from .views import *
from django.contrib.auth import views as auth
from django.conf import settings

app_name = 'accounts' 
urlpatterns = [
    path('inscription/', inscription, name='inscription'),
    path('inscription/confirmation/', lambda request: render(request, 'accounts/inscription_confirmation.html'), name='inscription_done'),
    path('connexion/', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    #path('index/', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/index/', dashboard_index, name='dashboard-index'),
    #path('test-send-email/', test_send_email, name='test_send_email'),

    # Page pour entrer email
    path(
        'mot-de-passe-oublie/',
        auth.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
        name='password_reset'
    ),
    # Page pour dire que l'email a été envoyé
    path(
        'mot-de-passe-oublie/confirmation/',
        auth.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'
    ),
    # Page pour réinitialiser le mot de passe
    path(
        'mot-de-passe-oublie/validation/<uidb64>/<token>/',
        auth.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    # Page pour dire que le mot de passe a été réinitialisé
    path(
        'mot-de-passe-oublie/termine/',
        auth.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'
    ),

    # Activation par email après inscription
    path('activate/<uidb64>/<token>/', activate, name='activate'),


]