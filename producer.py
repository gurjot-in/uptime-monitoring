import json
import re
import time

import requests
import schedule
from kafka import KafkaProducer

import settings.config_parser as config


class Producer(object):
    def __init__(self):
        self.producer = KafkaProducer(**config.kafka)

    def monitor_websites(self):
        for site in config.sites:
            url = site.get('url')
            check_string = site.get('check_string')
            check_interval = site.get('interval')
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
                        'check_string': check_string,
                        'regex_match': regex_match
                        })

        print(message)
        self.producer.send('helsinki', json.dumps(message).encode('utf-8'))


if __name__ == '__main__':
    producer = Producer()
    producer.monitor_websites()
