from django.core.management.base import BaseCommand, CommandError
from base.models import Task, User


class Command(BaseCommand):
    help = "Add a new task"

    def add_arguments(self, parser):
        parser.add_argument('--user', nargs='?', type=int)
        parser.add_argument('--title', nargs='?', type=str)
        parser.add_argument('--desc', help='Required for description of task!')

    def handle(self, *args, **options):
        if(options['user']):
            user_id = options['user']
        else:
            raise CommandError('User not specified!')

        if(options['title']):
            title = options['title']
        else:
            raise CommandError('Title not specified!')

        desc = ""
        if(options['desc']):
            desc = options['desc']

        try:
            user = User.users.get(pk=user_id)
            task = Task(user=user, title=title, description=desc)
            self.stdout.write(self.style.SUCCESS(
                f'Task {title} created successfully '))
            task.save()
        except:
            raise CommandError(f'Task {title} cannot be created')
