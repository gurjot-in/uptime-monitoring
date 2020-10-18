import json
import re
import time

import requests
import schedule
from kafka import KafkaProducer

from settings.config_parser import kafka_config, monitoring_config


class Producer(object):
    def __init__(self):
        self.producer = KafkaProducer(**kafka_config)

    @staticmethod
    def fetch_website_config():
        return monitoring_config

    def monitor_websites(self):
        website_config = self.fetch_website_config()
        url = website_config.get('url')
        check_string = website_config.get('check_string')
        check_interval = website_config.get('check_interval')
        schedule.every(int(check_interval)).seconds.do(self._run_job, url=url, check_string=check_string)

        while 1:
            schedule.run_pending()
            time.sleep(1)

    def _run_job(self, url, check_string):
        response = requests.get(url, timeout=5)
        regex_match = True if re.search(check_string, response.text) else False

        message = dict({'status_code': response.status_code,
                        'url': url,
                        'response_time': response.elapsed.total_seconds(),
                        'regex_match': regex_match
                        })

        print(message)
        self.producer.send('helsinki', json.dumps(message).encode('utf-8'))


if __name__ == '__main__':
    producer = Producer()
    producer.monitor_websites()
