import json
import re
import time

import requests
import schedule
from kafka import KafkaProducer
import logging
import settings.config_parser as config
import kafka.errors


class Producer(object):
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=config.kafka.get('bootstrap_servers'),
            security_protocol=config.kafka.get('security_protocol'),
            ssl_cafile=config.kafka.get('ssl_cafile'),
            ssl_certfile=config.kafka.get('ssl_certfile'),
            ssl_keyfile=config.kafka.get('ssl_keyfile'),
        )

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
        try:
            self.producer.send(config.kafka['topic'], json.dumps(message).encode('utf-8'))
        except kafka.errors.KafkaTimeoutError as kte:
            logging.error('Kafka timeout error {}'.format(kte))
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    producer = Producer()
    producer.monitor_websites()
