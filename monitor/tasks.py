from celery.utils.log import get_task_logger
from celery import shared_task

from django.db.models import  Min

from .utils import API_KEY, get_token_info
logger = get_task_logger(__name__)

@shared_task
def sum(a,b):
    return a+b

@shared_task
def import_volumes(token_id, address):
    from datetime import datetime, timezone, timedelta
    from .models import Volume, Token
    import requests
    import pandas as pd
    from decimal import Decimal

    token = Token.objects.get(id=token_id)
    start_timestamp = (datetime.today()).replace(tzinfo=timezone.utc).timestamp()

    date__min = token.volumes.aggregate(Min('date')).get('date__min')
    if date__min:
        start_timestamp = int(date__min.timestamp())
    while True:
        url = f"http://api.ethplorer.io/getTokenHistory/{address}?apiKey={API_KEY}&limit=1000&timestamp={start_timestamp}"
        s = requests.Session()
        r = s.get(url)
        data = r.json()
        txs = data.get('operations', [])
        tokenInfo = None
        q = 10 ** 18
        if "error" in data:
            logger.error(data.get('error'))
            break
        if not txs:
            break
        for row in txs:
            if not tokenInfo:
                tokenInfo = row['tokenInfo']
                q = 10 ** int(tokenInfo['decimals'])
            val = Decimal(row['value'])
            row['value'] = float(val / q)

            del row['tokenInfo']

        df = pd.DataFrame(txs)
        if not df.empty:
            df['date'] = pd.to_datetime(df['timestamp'], unit='s')
            df.drop(['from', 'to','transactionHash'], axis=1)
            new_start = df['timestamp'].min()


        if new_start != start_timestamp:
            start_timestamp = new_start
        else:
            break
        Volume.objects.bulk_create(
            Volume(type=str(row['type']), volume=Decimal(row['value']), date=row['date'], token=token) for _, row in df.iterrows()
        )
