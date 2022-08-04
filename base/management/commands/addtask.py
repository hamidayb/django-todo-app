from django.core.management.base import BaseCommand, CommandError
from base.models import Task, User


class Command(BaseCommand):
    help = "Add a new task"

    def add_arguments(self, parser):
        parser.add_argument('user', nargs='?', type=int)
        parser.add_argument('title', nargs='?', type=str)
        parser.add_argument('--d', help='Required for description of task!')


    def handle(self, *args, **options):           
        user_id = options['user']
        title = options['title']
        desc = ""
        if(options['d']):
            desc = options['d']
        try:
            user = User.users.get(pk=user_id)
            task = Task(user=user, title=title, description=desc)
            self.stdout.write(self.style.SUCCESS(f'Task {title} created successfully '))
            task.save()
        except:
            raise CommandError(f'Task {title} cannot be created')
        
        
