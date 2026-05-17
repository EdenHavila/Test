from django.db import migrations


def add_operations_and_industry_data(apps, schema_editor):
    Famille = apps.get_model('catalogue', 'Famille')
    Categorie = apps.get_model('catalogue', 'Categorie')
    SousCategorie = apps.get_model('catalogue', 'SousCategorie')
    Service = apps.get_model('catalogue', 'Service')

    seed = [
        {
            'famille': 'Énergie & Environnement',
            'categories': [
                {
                    'designation': 'Énergie',
                    'sous_categories': [
                        ('Service', 'Audit énergétique'),
                        ('Service', 'Installation solaire'),
                        ('Bien', 'Compteurs et onduleurs'),
                    ],
                },
                {
                    'designation': 'Environnement',
                    'sous_categories': [
                        ('Service', 'Gestion des déchets'),
                        ('Service', 'Traitement des eaux'),
                        ('Bien', 'Équipements de tri'),
                    ],
                },
            ],
        },
        {
            'famille': 'Maintenance Industrielle',
            'categories': [
                {
                    'designation': 'Machines',
                    'sous_categories': [
                        ('Service', 'Maintenance des machines'),
                        ('Service', 'Calibration équipements'),
                        ('Bien', 'Pièces industrielles'),
                    ],
                },
                {
                    'designation': 'Outillage',
                    'sous_categories': [
                        ('Service', 'Réparation outillage'),
                        ('Bien', 'Consommables techniques'),
                    ],
                },
            ],
        },
        {
            'famille': 'Sécurité Incendie',
            'categories': [
                {
                    'designation': 'Prévention',
                    'sous_categories': [
                        ('Service', 'Détection incendie'),
                        ('Service', 'Plans d évacuation'),
                        ('Bien', 'Signalisation de secours'),
                    ],
                },
                {
                    'designation': 'Équipements',
                    'sous_categories': [
                        ('Bien', 'Extincteurs'),
                        ('Service', 'Vérification extincteurs'),
                        ('Service', 'Maintenance alarmes'),
                    ],
                },
            ],
        },
        {
            'famille': 'Voyage & Déplacements',
            'categories': [
                {
                    'designation': 'Réservation',
                    'sous_categories': [
                        ('Service', 'Billetterie'),
                        ('Service', 'Hébergement'),
                        ('Service', 'Assistance voyage'),
                    ],
                },
                {
                    'designation': 'Missions',
                    'sous_categories': [
                        ('Bien', 'Titres de transport'),
                        ('Service', 'Logistique de mission'),
                    ],
                },
            ],
        },
    ]

    for family_seed in seed:
        famille, _ = Famille.objects.get_or_create(designation=family_seed['famille'])
        famille.reference = famille.designation[:3].upper()
        famille.save()

        for category_seed in family_seed['categories']:
            categorie, _ = Categorie.objects.get_or_create(designation=category_seed['designation'], famille=famille)
            categorie.reference = f"{famille.reference}-{categorie.designation[:3].upper()}"
            categorie.save()

            for type_value, sc_name in category_seed['sous_categories']:
                sous_categorie, _ = SousCategorie.objects.get_or_create(
                    categorie=categorie,
                    nom=sc_name,
                    defaults={'type': type_value},
                )
                sous_categorie.type = type_value
                sous_categorie.reference = f"{categorie.reference}-{sous_categorie.nom[:3].upper()}"
                sous_categorie.save()

    service_templates = {
        'Audit énergétique': ['Audit énergétique des bâtiments'],
        'Installation solaire': ['Étude et installation solaire'],
        'Gestion des déchets': ['Collecte et valorisation des déchets'],
        'Traitement des eaux': ['Traitement et assainissement des eaux'],
        'Maintenance des machines': ['Maintenance préventive des machines'],
        'Calibration équipements': ['Calibration et réglage des équipements'],
        'Réparation outillage': ['Réparation d outillage industriel'],
        'Détection incendie': ['Installation de systèmes de détection incendie'],
        'Plans d évacuation': ['Conception de plans d évacuation'],
        'Vérification extincteurs': ['Contrôle réglementaire des extincteurs'],
        'Maintenance alarmes': ['Maintenance des alarmes incendie'],
        'Billetterie': ['Réservation et émission de billets'],
        'Hébergement': ['Réservation d hébergement'],
        'Assistance voyage': ['Assistance aux déplacements professionnels'],
        'Logistique de mission': ['Organisation logistique des missions'],
    }

    for sous_categorie in SousCategorie.objects.select_related('categorie__famille').filter(
        type='Service',
        categorie__famille__designation__in=[
            'Énergie & Environnement',
            'Maintenance Industrielle',
            'Sécurité Incendie',
            'Voyage & Déplacements',
        ],
    ).order_by('categorie__famille__designation', 'categorie__designation', 'nom'):
        for index, designation in enumerate(service_templates.get(sous_categorie.nom, [f"Prestation {sous_categorie.nom}"]), start=1):
            Service.objects.get_or_create(
                categorie=sous_categorie.categorie,
                designation=designation,
                defaults={
                    'frequence': 'ponctuel',
                    'description': f"{designation} rattaché à la sous-catégorie {sous_categorie.nom}.",
                    'reference': f"{sous_categorie.reference}-{index:03d}",
                },
            )


def remove_operations_and_industry_data(apps, schema_editor):
    Service = apps.get_model('catalogue', 'Service')
    SousCategorie = apps.get_model('catalogue', 'SousCategorie')
    Categorie = apps.get_model('catalogue', 'Categorie')
    Famille = apps.get_model('catalogue', 'Famille')

    Service.objects.filter(
        categorie__famille__designation__in=[
            'Énergie & Environnement',
            'Maintenance Industrielle',
            'Sécurité Incendie',
            'Voyage & Déplacements',
        ]
    ).delete()

    SousCategorie.objects.filter(
        categorie__famille__designation__in=[
            'Énergie & Environnement',
            'Maintenance Industrielle',
            'Sécurité Incendie',
            'Voyage & Déplacements',
        ]
    ).delete()

    Categorie.objects.filter(
        famille__designation__in=[
            'Énergie & Environnement',
            'Maintenance Industrielle',
            'Sécurité Incendie',
            'Voyage & Déplacements',
        ]
    ).delete()

    Famille.objects.filter(designation__in=[
        'Énergie & Environnement',
        'Maintenance Industrielle',
        'Sécurité Incendie',
        'Voyage & Déplacements',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_add_more_catalogue_data'),
    ]

    operations = [
        migrations.RunPython(add_operations_and_industry_data, remove_operations_and_industry_data),
    ]
