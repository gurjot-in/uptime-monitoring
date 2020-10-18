import psycopg2
from psycopg2.extras import RealDictCursor

from settings.config_parser import postgres_config


class SiteMonitoring(object):
    TABLE_NAME = 'metrics'

    def __init__(self):
        uri = postgres_config['service_url']
        self._con = psycopg2.connect(uri)
        self._con.autocommit = True
        self._cursor = self._con.cursor(cursor_factory=RealDictCursor)

    def create_table(self):
        query = """CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                url VARCHAR NOT NULL,
                status_code SMALLINT NOT NULL,
                response_time DECIMAL NOT NULL,
                regex_match BOOLEAN,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );""".format(table_name=SiteMonitoring.TABLE_NAME)

        self._cursor.execute(query)

    def create(self, url, status_code, response_time, regex_match):
        query = """INSERT INTO {table_name} (url, status_code, response_time, regex_match)
                   VALUES ('{url}','{status_code}', '{response_time}', '{regex_match}'); """.format(
            table_name=SiteMonitoring.TABLE_NAME,
            url=url,
            status_code=status_code,
            response_time=response_time,
            regex_match=regex_match)

        print(query)
        print(self._cursor.execute(query))

    def check_table_exists(self):
        query = """SELECT * FROM information_schema.tables
                    WHERE table_name = '{table_name}'""".format(table_name=SiteMonitoring.TABLE_NAME)
        self._cursor.execute(query)
        return bool(self._cursor.rowcount)

    def drop_table(self):
        query = """DROP TABLE {table_name};""".format(table_name=SiteMonitoring.TABLE_NAME)
        self._cursor.execute(query)

    def get_records(self):
        query = """select * from {table_name}""".format(table_name=SiteMonitoring.TABLE_NAME)
        self._cursor.execute(query)
        return self._cursor.fetchall()
