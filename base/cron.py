from time import sleep
from .models import Time
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent


def convert_time():
    cron_state = json.load(open(f'{BASE_DIR}/base/cron_state.json'))
    offset = cron_state['count']
    limit = offset + 10
    dates = Time.objects.all()[offset:limit]

    if(cron_state['timezone'] == "PST"):
        for date in dates:
            date.timezone = "UTC"
        if(limit >= 100):
            cron_state['timezone'] = "UTC"

    elif(cron_state['timezone'] == "UTC"):
        for date in dates:
            date.timezone = "PST"
        if(limit >= 100):
            cron_state['timezone'] = "PST"

    Time.objects.bulk_update(dates, ['timezone'])

    cron_state['count'] = limit % 100

    logger.info(cron_state)
    
    with open(f'{BASE_DIR}/base/cron_state.json', "w") as json_file:
        json.dump(cron_state, json_file)
