"""Context processors exposant les indicateurs de rôle aux templates.

Fournir des booléens dans les templates garde les conditions lisibles
et évite de répéter les vérifications de groupes dans plusieurs vues.
"""
from .permissions import is_admin, is_gestionnaire, is_demandeur, can_access_settings


def role_flags(request):
    """Renvoie un petit dictionnaire de booléens de rôle disponibles dans les templates.

    Exemple dans un template : {% if is_gestionnaire_user %} ... {% endif %}
    """
    user = getattr(request, 'user', None)
    return {
        'is_admin_user': is_admin(user),
        'is_gestionnaire_user': is_gestionnaire(user),
        'is_demandeur_user': is_demandeur(user),
        'can_access_settings': can_access_settings(user),
    }
