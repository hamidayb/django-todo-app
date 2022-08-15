from django.core.management.base import BaseCommand, CommandError
from base.models import User
from django.contrib.auth.hashers import make_password



class Command(BaseCommand):
    help = "Add user"

    def add_arguments(self, parser):
        parser.add_argument('--email', nargs='?', type=str)
        parser.add_argument('--name', nargs='?', type=str)
        parser.add_argument('--age', nargs='?', type=int)
        parser.add_argument('--city', nargs='?', type=str)
        parser.add_argument('--pass', nargs='?', type=str)


    def handle(self, *args, **options):           
        if(options['email']):    
            email = options['email']
        else:
            raise CommandError('Email not specified!')

        if(options['name']):    
            name = options['name']
        else:
            raise CommandError('Name not specified!')

        if(options['pass']):    
            password = make_password(options['pass'])
        else:
            raise CommandError('Password not specified!')
            
        age = None
        city = None
        if(options['age']):    
            age = options['age']
        if(options['city']):    
            city = options['city']
        try:
            user = User(email=email, name=name, age=age, city=city, password=password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User {name} created successfully '))
        except:
            raise CommandError(f'Task {name} cannot be created')
        
        
