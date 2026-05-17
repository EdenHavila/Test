from django.db import migrations


def resync_catalogue(apps, schema_editor):
    SousCategorie = apps.get_model('catalogue', 'SousCategorie')
    Service = apps.get_model('catalogue', 'Service')

    type_by_name = {
        # Bien
        'Denrées alimentaires': 'Bien',
        'Ordinateurs': 'Bien',
        'Périphériques': 'Bien',
        'Imprimantes': 'Bien',
        'Baies réseau': 'Bien',
        'Pièces de rechange': 'Bien',
        'Véhicules utilitaires': 'Bien',
        # Service
        'Nettoyage de bureaux': 'Service',
        'Nettoyage industriel': 'Service',
        'Hygiène sanitaire': 'Service',
        'Gardiennage': 'Service',
        'Contrôle d accès': 'Service',
        'Vidéo surveillance': 'Service',
        'Traiteur événementiel': 'Service',
        'Cantine': 'Service',
        'Licences logicielles': 'Service',
        'SaaS': 'Service',
        'Maintenance applicative': 'Service',
        'Serveurs hébergés': 'Service',
        'Cloud computing': 'Service',
        'Plomberie': 'Service',
        'Électricité': 'Service',
        'Peinture': 'Service',
        'Maintenance préventive': 'Service',
        'Réparation équipements': 'Service',
        'Transport local': 'Service',
        'Location véhicules': 'Service',
        'Entrepôt': 'Service',
        'Manutention': 'Service',
        'Audit': 'Service',
        'Conseil RH': 'Service',
        'Conseil IT': 'Service',
        'Formation interne': 'Service',
        'Formation technique': 'Service',
    }

    service_templates = {
        'Nettoyage de bureaux': ['Nettoyage régulier de bureaux', 'Nettoyage approfondi des locaux'],
        'Nettoyage industriel': ['Nettoyage de sites industriels'],
        'Hygiène sanitaire': ['Assainissement des locaux'],
        'Gardiennage': ['Gardiennage de sites'],
        'Contrôle d accès': ['Contrôle d accès et filtrage'],
        'Vidéo surveillance': ['Installation de vidéosurveillance'],
        'Traiteur événementiel': ['Prestation traiteur pour événements'],
        'Cantine': ['Gestion de cantine collective'],
        'Licences logicielles': ['Gestion et renouvellement de licences'],
        'SaaS': ['Abonnement SaaS métier'],
        'Maintenance applicative': ['Maintenance corrective et évolutive'],
        'Serveurs hébergés': ['Hébergement de serveurs'],
        'Cloud computing': ['Services cloud et virtualisation'],
        'Plomberie': ['Interventions plomberie'],
        'Électricité': ['Maintenance électrique'],
        'Peinture': ['Travaux de peinture'],
        'Maintenance préventive': ['Maintenance préventive des équipements'],
        'Réparation équipements': ['Réparation et remise en service'],
        'Transport local': ['Transport de personnel et colis'],
        'Location véhicules': ['Location de véhicules utilitaires'],
        'Entrepôt': ['Mise à disposition d entrepôt'],
        'Manutention': ['Manutention et chargement'],
        'Audit': ['Audit organisationnel'],
        'Conseil RH': ['Conseil en ressources humaines'],
        'Conseil IT': ['Conseil en système d information'],
        'Formation interne': ['Formation interne du personnel'],
        'Formation technique': ['Formation technique spécialisée'],
    }

    for sous_categorie in SousCategorie.objects.select_related('categorie__famille').all().order_by('categorie__famille__designation', 'categorie__designation', 'nom'):
        expected_type = type_by_name.get(sous_categorie.nom)
        if expected_type:
            sous_categorie.type = expected_type
        if not sous_categorie.reference:
            sous_categorie.reference = f"{sous_categorie.categorie.reference}-{sous_categorie.nom[:3].upper()}"
        sous_categorie.save()

    # On repart sur une table Service vide.
    Service.objects.all().delete()

    for sous_categorie in SousCategorie.objects.select_related('categorie').filter(type='Service').order_by('categorie__famille__designation', 'categorie__designation', 'nom'):
        for index, designation in enumerate(service_templates.get(sous_categorie.nom, [f"Prestation {sous_categorie.nom}"]), start=1):
            Service.objects.create(
                categorie=sous_categorie.categorie,
                designation=designation,
                frequence='ponctuel',
                description=f"{designation} rattaché à la sous-catégorie {sous_categorie.nom}.",
                reference=f"{sous_categorie.reference}-{index:03d}",
            )


def reverse_resync(apps, schema_editor):
    Service = apps.get_model('catalogue', 'Service')
    Service.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_seed_catalogue'),
    ]

    operations = [
        migrations.RunPython(resync_catalogue, reverse_resync),
    ]
