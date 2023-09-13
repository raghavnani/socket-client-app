import logging
import random
import time
import pandas as pd
from ravenpackapi import RPApi, ApiConnectionError
from ravenpackapi import Dataset
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi(api_key="EagX12avS5DMLQgQjJ2wiQ")


# token = 'eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Imd6YXJ1YmluIn0.JhAa3AnYCRc5wkENsJw3XekdG1-pSHrP2IfCVZul0FFoZEc15lHqAdpI3wiwLj0jxFZVvVj4tRyVeZuk7dOjbg'
# headers = {
#     'Authorization': 'Bearer ' + token,
# }


df = pd.read_csv('raven_pack_tickers.csv')


def wait_between_attempts():
    """ Incremental backoff between connection attempts """
    wait_time = 0.3  # time is in seconds
    while True:
        yield wait_time
        wait_time = min(wait_time * 1.5, 30)
        wait_time *= (100 + random.randint(0, 50)) / 100

class Raven:

    def __init__(self) -> None:
        pass
    # query the realtime feed
        self.ds = api.create_dataset(
        Dataset(
            **{
                "product": "rpa",
                "product_version": "1.0",
                "name": "Events in US",
                "frequency": "granular",
            }
        )
        )

        self.wait_time = wait_between_attempts()



    def raven_pack(self, SEARCH_STRING,
                    ENTITY_NAME,
                    TOPIC,
                    GROUP,
                    TYPE,
                    FACT_LEVEL,
                    CATEGORY,
                    SOURCE_NAME):


        query_list = [{
                            "country_code": {
                                "$in": [
                                    "US"
                                ]
                            }
                        }]

        if SEARCH_STRING:
            query_list.append({
                                "headline": {
                                    "$search": SEARCH_STRING ,
                                }
                            })
        if ENTITY_NAME:
            query_list.append({
                            "entity_name": {
                                "$in": ENTITY_NAME.split(',') ,
                            }
                        })

        if TOPIC:
            query_list.append({
                            "topic": {
                                "$in": TOPIC.split(',') ,
                            }
                        })

        if GROUP:
            query_list.append({
                            "group": {
                                "$in": [GROUP] ,
                            }
                        })

        if TYPE:
            query_list.append({
                            "type": {
                                "$in": TYPE.split(',') ,
                            }
                        })

        if CATEGORY:
            query_list.append({
                            "category": {
                                "$in": CATEGORY.split(',') ,
                            }
                        })
        if SOURCE_NAME:
            query_list.append({
                            "source_name": {
                                "$search": SOURCE_NAME.split(',') ,
                            }
                        })
        if FACT_LEVEL:
            query_list.append({
                            "fact_level": {
                                "$search": FACT_LEVEL.split(','),
                            }
                        })

        

        # query the realtime feed

        self.ds.delete()
        new_ds = api.create_dataset(
        Dataset(
            **{
                "product": "rpa",
                "product_version": "1.0",
                "name": "Events in US",
                "filters": {
                    "$and": query_list
                },
                "frequency": "granular",
            }
        )
        )

        del self.ds

        self.ds = new_ds

        self.connect(True)

    def connect(self, check=False):
        while True:
            try:
                for record in self.ds.request_realtime():

                    try:

                        ticker = df[df['RP_ENTITY_ID'] == record['RP_ENTITY_ID']]['DATA_VALUE'].values[0]
                    except:
                        ticker = None
                    
                    
                    if ticker:

                        event = 'binary_regex_test'


                        if event:

                            if record['EVENT_SENTIMENT_SCORE']:
                                EVENT_SENTIMENT_SCORE =   str(round(record['EVENT_SENTIMENT_SCORE'],2))
                            else:
                                EVENT_SENTIMENT_SCORE =   str(record['EVENT_SENTIMENT_SCORE'])



                            payload = {
                                'TIMESTAMP_UTC':   str(record['TIMESTAMP_UTC']),
                                'RP_ENTITY_ID':   record['RP_ENTITY_ID'],
                                'ENTITY_NAME':   record['ENTITY_NAME'],
                                'TOPIC':   record['TOPIC'],
                                'GROUP':   record['GROUP'],
                                'TYPE':   record['TYPE'],
                                'FACT_LEVEL':   record['FACT_LEVEL'],
                                'CATEGORY':   record['CATEGORY'],
                                'SOURCE_NAME':   record['SOURCE_NAME'],
                                'HEADLINE':   record['HEADLINE'],
                                'EVENT_RELEVANCE':   str(record['EVENT_RELEVANCE']),
                                'EVENT_SENTIMENT_SCORE' : EVENT_SENTIMENT_SCORE,
                                'signals': {
                                    'ticker': ticker,
                                    'event':   event,

                                }
                            }

                            # print(payload)

                            requests.post('http://104.131.126.10:5200/api/send', json=payload)


            except (KeyboardInterrupt, SystemExit):
                break
            except ApiConnectionError as e:
                logger.error("Connection error %s: reconnecting..." % e)
                time.sleep(next(self.wait_time))
