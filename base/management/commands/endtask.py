from django.core.management.base import BaseCommand, CommandError
from base.models import Task

class Command(BaseCommand):
    help = "Set task to complete or delete it"

    def add_arguments(self, parser):
        parser.add_argument('task_ids', nargs='+', type=int)
        parser.add_argument('--d', action='store_true', help='Delete task or tasks instead of ending them',)

    def handle(self, *args, **options):            
        for task_id in options['task_ids']:
            try:
                task = Task.tasks.get(pk=task_id)
            except Task.DoesNotExist:
                raise CommandError('Task "%s" does not exist' % task_id)
            
            if(options['d']):
                task.delete()
            else:
                task.complete = True
                task.save()
            

            self.stdout.write(self.style.SUCCESS('Task "%s" set to complete ' % task_id))
