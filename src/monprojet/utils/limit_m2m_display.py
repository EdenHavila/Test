#à utiliser pour limiter l'affichage des champs ManyToMany dans les templates Django
def limit_m2m_display(qs, limit=2, field_name='nom'):
    """
    Limite l'affichage d'un queryset ManyToMany.

    :param qs: QuerySet (ex: fournisseur.types.all())
    :param limit: nombre max d'éléments affichés
    :param field_name: champ à afficher (ex: 'nom')
    :return: dict
    """
    total = qs.count()
    displayed = qs[:limit]

    values = list(displayed.values_list(field_name, flat=True))
    remaining = max(total - limit, 0)

    return {
        'values': values,
        'remaining': remaining,
        'total': total
    }
"""
Exemple d'utilisation dans un template Django :
{% with specialites_data=limit_m2m_display(fournisseur.specialite.all(), limit=2, field_name='nom') %}
    {% for specialite in specialites_data.values %}
        {{ specialite }}{% if not forloop.last %}, {% endif %}
    {% endfor %}
    {% if specialites_data.remaining > 0 %}
        et {{ specialites_data.remaining }} autres
    {% endif %}
{% endwith %}
"""
"""
Exemple d'appel dans une vue Django :
from monprojet.utils.limit_m2m_display import limit_m2m_display
from django.shortcuts import render
from .models import Fournisseur

def liste_fournisseurs(request):
    # Précharger les relations ManyToMany pour éviter N+1
    fournisseurs = Fournisseur.objects.prefetch_related('types', 'specialite').all()

    # Préparer les données pour le template
    fournisseurs_data = []
    for f in fournisseurs:
        fournisseurs_data.append({
            'fournisseur': f,
            'types_data': limit_m2m_display(f.types.all(), limit=2, field_name='nom'),
            'specialites_data': limit_m2m_display(f.specialite.all(), limit=2, field_name='nom')
        })

    context = {
        'fournisseurs_data': fournisseurs_data
    }

    return render(request, 'Fournisseur/partials/liste_fournisseurs.html', context)

"""

"""
Exemple d'utilisation dans un template Django avec le contexte préparé dans la vue :
{% for item in fournisseurs_data %}
    <tr>
        <td>{{ item.fournisseur.nom }}</td>
        <td>
            {% for type in item.types_data.values %}
                {{ type }}{% if not forloop.last %}, {% endif %}
            {% endfor %}
            {% if item.types_data.remaining > 0 %}
                et {{ item.types_data.remaining }} autres
            {% endif %}
        </td>
        <td>
            {% for specialite in item.specialites_data.values %}
                {{ specialite }}{% if not forloop.last %}, {% endif %}
            {% endfor %}
            {% if item.specialites_data.remaining > 0 %}
                + {{ item.specialites_data.remaining }} autres
            {% endif %}
        </td>
    </tr>
{% endfor %}
"""