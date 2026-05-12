"""Management command to create a demo 'Demandeur' user for testing.

Usage (from project root):
    python manage.py create_demo_user --username demo_demandeur --email demo@example.com

This command does three things:
1. Ensures the Django Group 'Demandeur' exists.
2. Ensures the Role model has an entry for 'demandeur' (kept for UI/business display).
3. Creates a new user with the provided username/email and adds it to the 'Demandeur' group.

Security note:
- The default password created by this command should be changed immediately in a real environment.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from django.conf import settings


class Command(BaseCommand):
    help = "Create a demo user assigned to the 'Demandeur' role/group"

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='demo_demandeur', help='Username for the demo user')
        parser.add_argument('--email', type=str, default='demo@example.com', help='Email for the demo user')
        parser.add_argument('--password', type=str, default='Demandeur123!', help='Password for the demo user')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Import models lazily to avoid startup issues if Django isn't fully configured.
        try:
            from accounts.models import User, Role
        except Exception as exc:
            raise CommandError(f"Could not import accounts models: {exc}")

        # 1) Ensure Group exists
        group_name = 'Demandeur'
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created group '{group_name}'"))
        else:
            self.stdout.write(f"Group '{group_name}' already exists")

        # 2) Ensure Role (UI field) exists. Role.nom_role choices use lowercase values.
        role_name = 'demandeur'
        role_obj, role_created = Role.objects.get_or_create(nom_role=role_name)
        if role_created:
            self.stdout.write(self.style.SUCCESS(f"Created Role entry '{role_name}'"))
        else:
            self.stdout.write(f"Role entry '{role_name}' already exists")

        # 3) Create or update the demo user
        user, user_created = User.objects.get_or_create(username=username, defaults={
            'email': email,
        })

        if user_created:
            user.set_password(password)
            user.email = email
            user.is_active = True
            # Keep is_staff False for Demandeur (no admin site access)
            user.is_staff = False
            user.is_superuser = False
            # assign the Role FK for UI display
            user.role = role_obj
            user.save()
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f"Created user '{username}' with password '{password}'"))
        else:
            # If the user exists, ensure membership and role are set.
            changed = False
            if user.email != email:
                user.email = email
                changed = True
            if user.role != role_obj:
                user.role = role_obj
                changed = True
            if not user.groups.filter(name=group_name).exists():
                user.groups.add(group)
                changed = True
            if changed:
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Updated existing user '{username}' and assigned to group '{group_name}'"))
            else:
                self.stdout.write(f"User '{username}' already exists and is up-to-date")

        self.stdout.write(self.style.NOTICE("Demo user creation finished. Change the password upon first login."))
