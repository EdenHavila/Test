from django.db import migrations


def add_more_catalogue_data(apps, schema_editor):
    Famille = apps.get_model('catalogue', 'Famille')
    Categorie = apps.get_model('catalogue', 'Categorie')
    SousCategorie = apps.get_model('catalogue', 'SousCategorie')
    Service = apps.get_model('catalogue', 'Service')

    extra_catalogue = [
        {
            'famille': 'Achats & Approvisionnement',
            'categories': [
                {
                    'designation': 'Fournitures',
                    'sous_categories': [
                        ('Bien', 'Papeterie'),
                        ('Bien', 'Consommables de bureau'),
                        ('Bien', 'Petits équipements'),
                    ],
                },
                {
                    'designation': 'Prestations',
                    'sous_categories': [
                        ('Service', 'Sourcing fournisseurs'),
                        ('Service', 'Négociation commerciale'),
                        ('Service', 'Gestion des appels d offres'),
                    ],
                },
            ],
        },
        {
            'famille': 'Ressources Humaines',
            'categories': [
                {
                    'designation': 'Recrutement',
                    'sous_categories': [
                        ('Service', 'Sourcing candidats'),
                        ('Service', 'Entretiens de sélection'),
                        ('Service', 'Intégration des nouveaux employés'),
                    ],
                },
                {
                    'designation': 'Administration du personnel',
                    'sous_categories': [
                        ('Service', 'Gestion des dossiers RH'),
                        ('Service', 'Paie et déclarations sociales'),
                        ('Service', 'Gestion des absences'),
                    ],
                },
            ],
        },
        {
            'famille': 'Communication & Marketing',
            'categories': [
                {
                    'designation': 'Communication',
                    'sous_categories': [
                        ('Service', 'Création de contenus'),
                        ('Service', 'Relations presse'),
                        ('Service', 'Gestion réseaux sociaux'),
                    ],
                },
                {
                    'designation': 'Marketing',
                    'sous_categories': [
                        ('Service', 'Campagnes publicitaires'),
                        ('Service', 'Études de marché'),
                        ('Service', 'Événementiel marketing'),
                    ],
                },
            ],
        },
        {
            'famille': 'Juridique & Conformité',
            'categories': [
                {
                    'designation': 'Conseil juridique',
                    'sous_categories': [
                        ('Service', 'Rédaction de contrats'),
                        ('Service', 'Consultation juridique'),
                        ('Service', 'Contentieux'),
                    ],
                },
                {
                    'designation': 'Conformité',
                    'sous_categories': [
                        ('Service', 'Veille réglementaire'),
                        ('Service', 'Audit de conformité'),
                    ],
                },
            ],
        },
    ]

    for family_seed in extra_catalogue:
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
        'Sourcing fournisseurs': ['Qualification des fournisseurs'],
        'Négociation commerciale': ['Appui à la négociation'],
        'Gestion des appels d offres': ['Préparation et suivi des AO'],
        'Sourcing candidats': ['Recherche de profils'],
        'Entretiens de sélection': ['Conduite des entretiens'],
        'Intégration des nouveaux employés': ['Onboarding collaborateurs'],
        'Gestion des dossiers RH': ['Administration des dossiers RH'],
        'Paie et déclarations sociales': ['Traitement de la paie'],
        'Gestion des absences': ['Suivi des congés et absences'],
        'Création de contenus': ['Rédaction de contenus corporate'],
        'Relations presse': ['Gestion des relations médias'],
        'Gestion réseaux sociaux': ['Animation des réseaux sociaux'],
        'Campagnes publicitaires': ['Gestion des campagnes media'],
        'Études de marché': ['Analyse et veille marché'],
        'Événementiel marketing': ['Organisation d événements promotionnels'],
        'Rédaction de contrats': ['Rédaction contractuelle'],
        'Consultation juridique': ['Conseil juridique ponctuel'],
        'Contentieux': ['Accompagnement contentieux'],
        'Veille réglementaire': ['Suivi des évolutions réglementaires'],
        'Audit de conformité': ['Audit conformité interne'],
    }

    new_service_scs = SousCategorie.objects.select_related('categorie__famille').filter(
        type='Service',
        categorie__famille__designation__in=[
            'Achats & Approvisionnement',
            'Ressources Humaines',
            'Communication & Marketing',
            'Juridique & Conformité',
        ]
    ).order_by('categorie__famille__designation', 'categorie__designation', 'nom')

    for sous_categorie in new_service_scs:
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


def remove_more_catalogue_data(apps, schema_editor):
    Service = apps.get_model('catalogue', 'Service')
    SousCategorie = apps.get_model('catalogue', 'SousCategorie')
    Categorie = apps.get_model('catalogue', 'Categorie')
    Famille = apps.get_model('catalogue', 'Famille')

    Service.objects.filter(
        categorie__famille__designation__in=[
            'Achats & Approvisionnement',
            'Ressources Humaines',
            'Communication & Marketing',
            'Juridique & Conformité',
        ]
    ).delete()

    SousCategorie.objects.filter(
        categorie__famille__designation__in=[
            'Achats & Approvisionnement',
            'Ressources Humaines',
            'Communication & Marketing',
            'Juridique & Conformité',
        ]
    ).delete()

    Categorie.objects.filter(
        famille__designation__in=[
            'Achats & Approvisionnement',
            'Ressources Humaines',
            'Communication & Marketing',
            'Juridique & Conformité',
        ]
    ).delete()

    Famille.objects.filter(designation__in=[
        'Achats & Approvisionnement',
        'Ressources Humaines',
        'Communication & Marketing',
        'Juridique & Conformité',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_resync_services_and_types'),
    ]

    operations = [
        migrations.RunPython(add_more_catalogue_data, remove_more_catalogue_data),
    ]
