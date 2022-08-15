from django.core.management.base import BaseCommand, CommandError
from base.models import Time
from datetime import datetime
from django.utils import timezone
import pytz


class Command(BaseCommand):
    help = "Add PST Time to DB"

    def handle(self, *args, **options):
        pst_times = []
        for i in range(1, 101):
            date = datetime.now(pytz.timezone("US/Pacific"))
            pst_times.append(Time(id=i, time=date))

        try:
            Time.objects.all().delete()
            Time.objects.bulk_create(pst_times)
            self.stdout.write(self.style.SUCCESS(
                f'Dates added successfully created successfully ')
            )
        except Exception as e:
            raise CommandError(f'ERROR => {e}')
