import json

from kafka import KafkaConsumer

import db
import settings.config_parser as config


class Consumer(object):
    def __init__(self):
        self.consumer = KafkaConsumer("helsinki", **config.kafka)
        self._metric_db = db.SiteMonitoring()

        if not self._metric_db.check_table_exists():
            self._metric_db.create_table()

    def run(self):

        print(self._metric_db.get_records())
        for msg in self.consumer:
            msg = json.loads(msg.value.decode('utf-8'))
            print("Received: {}".format(msg))
            self._metric_db.create(url=msg.get('url'),
                                   status_code=msg.get('status_code'),
                                   check_string=msg.get('check_string'),
                                   response_time=msg.get('response_time'),
                                   regex_match=msg.get('regex_match')
                                   )


if __name__ == '__main__':
    consumer = Consumer()
    consumer.run()
