from django.core.management.base import BaseCommand
from base.models import User


class Command(BaseCommand):
    help = "Show all users"

    def handle(self, *args, **options):
        users = User.users.all()
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('{:^60}'.format("ALL USERS")))
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS(
            '{:3} {:20} {:20} {:5} {:20}'.format("ID", "Name", "Email", "Age", "City")))
        for user in users:
            self.stdout.write('{:<3} {:20} {:20} {:5} {:20}'.format(
                user.id, user.name, user.email, str(user.age), str(user.city)))
        self.stdout.write('\n')
