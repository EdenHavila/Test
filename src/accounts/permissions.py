"""Aides et décorateurs d'autorisation pour le contrôle d'accès par rôle.

Ce module centralise les vérifications de rôle afin que le reste du projet
utilise une seule source de vérité (Groupes Django + is_staff/is_superuser).

Règles recommandées :
- Conserver `accounts.models.User.role` uniquement pour l'affichage métier.
- Utiliser ces aides pour les décorateurs de vues et les vérifications internes.
"""
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    """Renvoie True si l'utilisateur est un administrateur.

    On considère comme administrateur un superutilisateur Django ou un membre
    du groupe "Admin" pour le contrôle d'accès applicatif.
    """
    try:
        return bool(user and user.is_authenticated and (user.is_superuser or user.groups.filter(name="Admin").exists()))
    except Exception:
        return False


def is_gestionnaire(user):
    """Renvoie True si l'utilisateur appartient au groupe Gestionnaire."""
    try:
        return bool(user and user.is_authenticated and user.groups.filter(name="Gestionnaire").exists())
    except Exception:
        return False


def is_demandeur(user):
    """Renvoie True si l'utilisateur appartient au groupe Demandeur."""
    try:
        return bool(user and user.is_authenticated and user.groups.filter(name="Demandeur").exists())
    except Exception:
        return False


def can_access_settings(user):
    """Renvoie True si l'utilisateur peut accéder aux paramètres du projet (/admin/).

    On utilise `is_staff` car l'admin Django s'appuie sur ce drapeau.
    """
    try:
        return bool(user and user.is_authenticated and user.is_staff)
    except Exception:
        return False


# Décorateurs -------------------------------------------------------------
def admin_required(view_func):
    """Décorateur qui autorise uniquement les administrateurs."""
    return user_passes_test(is_admin)(view_func)


def gestionnaire_or_admin_required(view_func):
    """Décorateur qui autorise un gestionnaire ou un administrateur."""
    return user_passes_test(lambda u: is_admin(u) or is_gestionnaire(u))(view_func)


def any_role_required(view_func):
    """Décorateur qui autorise Demandeur, Gestionnaire ou Admin.

    À utiliser pour les pages destinées à tous les acteurs authentifiés du flux
    métier, par exemple le tableau de bord.
    """
    return user_passes_test(lambda u: is_admin(u) or is_gestionnaire(u) or is_demandeur(u))(view_func)


def require_role_check(check_func):
    """Renvoie un décorateur qui applique une fonction booléenne personnalisée `check_func(user)`.

    Cette aide permet de faire des contrôles de rôle ponctuels tout en gardant
    une convention cohérente pour les décorateurs.
    """
    def decorator(view_func):
        return user_passes_test(check_func)(view_func)
    return decorator
