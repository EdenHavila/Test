from django.db import migrations


def seed_catalogue(apps, schema_editor):
	Famille = apps.get_model('catalogue', 'Famille')
	Categorie = apps.get_model('catalogue', 'Categorie')
	SousCategorie = apps.get_model('catalogue', 'SousCategorie')
	Service = apps.get_model('catalogue', 'Service')

	# Supprimer les services existants pour repartir sur une base cohérente métier.
	Service.objects.all().delete()

	catalogue = [
		{
			'famille': 'Services Généraux',
			'categories': [
				{
					'designation': 'Nettoyage',
					'sous_categories': [
						('Service', 'Nettoyage de bureaux'),
						('Service', 'Nettoyage industriel'),
						('Service', 'Hygiène sanitaire'),
					],
				},
				{
					'designation': 'Sécurité',
					'sous_categories': [
						('Service', 'Gardiennage'),
						('Service', 'Contrôle d accès'),
						('Service', 'Vidéo surveillance'),
					],
				},
				{
					'designation': 'Restauration',
					'sous_categories': [
						('Bien', 'Denrées alimentaires'),
						('Service', 'Traiteur événementiel'),
						('Service', 'Cantine'),
					],
				},
			],
		},
		{
			'famille': 'Informatique',
			'categories': [
				{
					'designation': 'Matériel',
					'sous_categories': [
						('Bien', 'Ordinateurs'),
						('Bien', 'Périphériques'),
						('Bien', 'Imprimantes'),
					],
				},
				{
					'designation': 'Logiciels',
					'sous_categories': [
						('Service', 'Licences logicielles'),
						('Service', 'SaaS'),
						('Service', 'Maintenance applicative'),
					],
				},
				{
					'designation': 'Infrastructure',
					'sous_categories': [
						('Bien', 'Baies réseau'),
						('Service', 'Serveurs hébergés'),
						('Service', 'Cloud computing'),
					],
				},
			],
		},
		{
			'famille': 'Maintenance',
			'categories': [
				{
					'designation': 'Bâtiment',
					'sous_categories': [
						('Service', 'Plomberie'),
						('Service', 'Électricité'),
						('Service', 'Peinture'),
					],
				},
				{
					'designation': 'Équipements',
					'sous_categories': [
						('Service', 'Maintenance préventive'),
						('Service', 'Réparation équipements'),
						('Bien', 'Pièces de rechange'),
					],
				},
			],
		},
		{
			'famille': 'Transport & Logistique',
			'categories': [
				{
					'designation': 'Transport',
					'sous_categories': [
						('Service', 'Transport local'),
						('Service', 'Location véhicules'),
						('Bien', 'Véhicules utilitaires'),
					],
				},
				{
					'designation': 'Stockage',
					'sous_categories': [
						('Service', 'Entrepôt'),
						('Service', 'Manutention'),
					],
				},
			],
		},
		{
			'famille': 'Services Professionnels',
			'categories': [
				{
					'designation': 'Conseil',
					'sous_categories': [
						('Service', 'Audit'),
						('Service', 'Conseil RH'),
						('Service', 'Conseil IT'),
					],
				},
				{
					'designation': 'Formation',
					'sous_categories': [
						('Service', 'Formation interne'),
						('Service', 'Formation technique'),
					],
				},
			],
		},
	]

	# Création ou mise à jour des familles / catégories / sous-catégories.
	for family_seed in catalogue:
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

	# Recréer les services uniquement pour les sous-catégories de type Service.
	service_templates = {
		'Nettoyage de bureaux': ['Nettoyage régulier de bureaux'],
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

	service_type_scs = SousCategorie.objects.select_related('categorie__famille').filter(type='Service').order_by('categorie__famille__designation', 'categorie__designation', 'nom')
	for sous_categorie in service_type_scs:
		services = service_templates.get(sous_categorie.nom, [f"Prestation {sous_categorie.nom}"])
		for index, designation in enumerate(services, start=1):
			reference = f"{sous_categorie.reference}-{index:03d}"
			Service.objects.create(
				categorie=sous_categorie.categorie,
				designation=designation,
				frequence='ponctuel',
				description=f"{designation} rattaché à la sous-catégorie {sous_categorie.nom}.",
				reference=reference,
			)


def unseed_catalogue(apps, schema_editor):
	Service = apps.get_model('catalogue', 'Service')
	SousCategorie = apps.get_model('catalogue', 'SousCategorie')
	Categorie = apps.get_model('catalogue', 'Categorie')
	Famille = apps.get_model('catalogue', 'Famille')

	Service.objects.all().delete()
	SousCategorie.objects.filter(nom__in=[
		'Nettoyage de bureaux', 'Nettoyage industriel', 'Hygiène sanitaire',
		'Gardiennage', 'Contrôle d accès', 'Vidéo surveillance',
		'Traiteur événementiel', 'Cantine', 'Licences logicielles', 'SaaS',
		'Maintenance applicative', 'Serveurs hébergés', 'Cloud computing',
		'Plomberie', 'Électricité', 'Peinture', 'Maintenance préventive',
		'Réparation équipements', 'Transport local', 'Location véhicules',
		'Entrepôt', 'Manutention', 'Audit', 'Conseil RH', 'Conseil IT',
		'Formation interne', 'Formation technique', 'Denrées alimentaires',
		'Ordinateurs', 'Périphériques', 'Imprimantes', 'Baies réseau',
		'Pièces de rechange', 'Véhicules utilitaires',
	]).delete()

	Categorie.objects.filter(designation__in=[
		'Nettoyage', 'Sécurité', 'Restauration', 'Matériel', 'Logiciels',
		'Infrastructure', 'Bâtiment', 'Équipements', 'Transport', 'Stockage',
		'Conseil', 'Formation'
	]).delete()

	Famille.objects.filter(designation__in=[
		'Services Généraux', 'Informatique', 'Maintenance', 'Transport & Logistique', 'Services Professionnels'
	]).delete()


class Migration(migrations.Migration):

	dependencies = [
		('catalogue', '0001_initial'),
	]

	operations = [
		migrations.RunPython(seed_catalogue, unseed_catalogue),
	]

