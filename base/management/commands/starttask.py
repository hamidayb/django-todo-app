from django.core.management.base import BaseCommand, CommandError
from base.models import Task

class Command(BaseCommand):
    help = "Set task to incomplete"

    def add_arguments(self, parser):
        parser.add_argument('task_ids', nargs='*', type=int)


    def handle(self, *args, **options):
        for task_id in options['task_ids']:
            try:
                task = Task.tasks.get(pk=task_id)
            except Task.DoesNotExist:
                raise CommandError('Task "%s" does not exist' % task_id)

            task.complete = False
            task.save()

            self.stdout.write(self.style.SUCCESS('Task "%s" set to incomplete ' % task_id))
