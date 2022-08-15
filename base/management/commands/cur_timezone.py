from django.core.management.base import BaseCommand
from datetime import date, datetime


class Command(BaseCommand):
    help = "Current Timezone"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(datetime.now()))
