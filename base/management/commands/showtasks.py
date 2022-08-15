from django.core.management.base import BaseCommand
from base.models import Task, User


class Command(BaseCommand):
    help = "Show all tasks"

    def handle(self, *args, **options):
        tasks = Task.tasks.all()
        self.stdout.write('='*96)
        self.stdout.write(self.style.SUCCESS('{:^96}'.format("ALL TASKS")))
        self.stdout.write('='*96)
        self.stdout.write(self.style.SUCCESS('{:3} {:20} {:30} {:30} {:10}'.format(
            "ID", "User Name", "Title", "Description", "Completed")))
        for task in tasks:
            self.stdout.write('{:<3} {:20} {:30} {:30} {:10}'.format(task.id, str(
                task.user), task.title, str(task.description), str(task.complete)))
        self.stdout.write('\n')
