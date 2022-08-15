from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    help = "Reset cron state"

    def add_arguments(self, parser):
        parser.add_argument('--a', action='store_true', help='Delete data in app.log',)


    def handle(self, *args, **options):
        try:
            cron_state = json.load(open(f'{BASE_DIR}/base/cron_state.json'))
            cron_state['count'] = 0
            cron_state['timezone'] = "PST"
            with open(f'{BASE_DIR}/base/cron_state.json', "w") as json_file:
                json.dump(cron_state, json_file)

            if(options['a']):
                f = open(f'{BASE_DIR}/log/app.log', 'w')
                f.close()
            self.stdout.write(self.style.SUCCESS(
                'Resetted successfully')
            )
        except Exception as e:
            raise CommandError(f'ERROR => {e}')
