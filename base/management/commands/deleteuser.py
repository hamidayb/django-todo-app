from django.core.management.base import BaseCommand, CommandError
from base.models import User
from django.contrib.auth.hashers import make_password



class Command(BaseCommand):
    help = "Add user"

    def add_arguments(self, parser):
        parser.add_argument('user_ids', nargs='+', type=int)        


    def handle(self, *args, **options):
        for user_id in options['user_ids']:
            try:
                user = User.users.get(pk=user_id)
                user.delete()
                self.stdout.write(self.style.SUCCESS(f'User {user} deleted successfully!'))
            except User.DoesNotExist:
                raise CommandError(f'User {user_id} doesn\'t exists')
                
        
