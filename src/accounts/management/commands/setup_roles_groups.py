"""Crée les groupes et entrées Role standards, puis synchronise éventuellement les utilisateurs.

Cette commande garantit la présence des groupes suivants dans le projet :
- Admin
- Gestionnaire
- Demandeur

Elle garantit aussi que la table `accounts.models.Role` contient les
entrées correspondantes (valeurs `nom_role` : 'admin', 'gestionnaire', 'demandeur'),
conservées uniquement pour l'affichage métier.

Options :
- --sync-users : pour chaque utilisateur ayant `user.role`, l'ajouter au groupe correspondant.
- --make-admins-staff : définir `is_staff=True` pour les utilisateurs du groupe Admin (utile pour l'accès à l'admin).

Usage:
    python manage.py setup_roles_groups --sync-users --make-admins-staff

Note : cette commande ajoute uniquement les groupes/rôles et affecte les utilisateurs aux groupes ;
elle ne supprime aucune appartenance existante afin d'éviter de casser des configurations manuelles.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Créer les groupes standards + les entrées Role, puis synchroniser éventuellement les utilisateurs"

    def add_arguments(self, parser):
        parser.add_argument('--sync-users', action='store_true', help='Sync existing users into groups according to user.role')
        parser.add_argument('--make-admins-staff', action='store_true', help='Set is_staff=True for users in Admin group')

    def handle(self, *args, **options):
        try:
            from accounts.models import Role, User
        except Exception as exc:
            raise CommandError(f"Could not import accounts models: {exc}")

        # Correspondance : nom du groupe affiché -> valeur Role.nom_role
        mapping = [
            ("Admin", "admin"),
            ("Gestionnaire", "gestionnaire"),
            ("Demandeur", "demandeur"),
        ]

        created_groups = []
        for group_name, role_code in mapping:
            group, g_created = Group.objects.get_or_create(name=group_name)
            if g_created:
                self.stdout.write(self.style.SUCCESS(f"Created group '{group_name}'"))
            else:
                self.stdout.write(f"Group '{group_name}' already exists")
            created_groups.append(group_name)

            # S'assurer que l'entrée Role existe (champ utilisé pour l'affichage métier)
            role_obj, r_created = Role.objects.get_or_create(nom_role=role_code)
            if r_created:
                self.stdout.write(self.style.SUCCESS(f"Created Role entry '{role_code}'"))
            else:
                self.stdout.write(f"Role entry '{role_code}' already exists")

        if options['sync_users']:
            users = User.objects.all()
            for user in users:
                role = getattr(user, 'role', None)
                if role and getattr(role, 'nom_role', None):
                    expected_group_name = role.nom_role.capitalize()
                    try:
                        group = Group.objects.get(name=expected_group_name)
                        if not user.groups.filter(name=expected_group_name).exists():
                            user.groups.add(group)
                            self.stdout.write(self.style.SUCCESS(f"Added user '{user.username}' to group '{expected_group_name}'"))
                    except Group.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Expected group '{expected_group_name}' not found for user '{user.username}'"))

        if options['make_admins_staff']:
            try:
                admin_group = Group.objects.get(name='Admin')
            except Group.DoesNotExist:
                self.stdout.write(self.style.WARNING("Admin group does not exist; cannot set is_staff"))
            else:
                admins = User.objects.filter(groups=admin_group)
                for u in admins:
                    if not u.is_staff:
                        u.is_staff = True
                        u.save()
                        self.stdout.write(self.style.SUCCESS(f"Set is_staff=True for '{u.username}'"))

        self.stdout.write(self.style.NOTICE("setup_roles_groups terminé"))
