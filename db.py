import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import settings.config_parser as config


class SiteMonitoring(object):
    TABLE_NAME = 'metrics'

    @staticmethod
    def _execute_sql(query):
        try:
            con = psycopg2.connect(config.postgres.get('service_url'))
        except psycopg2.OperationalError as e:
            logging.error('Postgres connection error {}'.format(e))
        except Exception as e:
            logging.error(e)
        else:
            cursor = con.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)
            return cursor, con

    def create_table(self):
        query = """CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                url VARCHAR NOT NULL,
                status_code SMALLINT NOT NULL,
                response_time DECIMAL NOT NULL,
                check_string VARCHAR NOT NULL, 
                regex_match BOOLEAN,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );""".format(table_name=SiteMonitoring.TABLE_NAME)

        cursor, con = self._execute_sql(query)
        cursor.close()
        con.close()

    def create(self, url, status_code, check_string, response_time, regex_match):
        query = """INSERT INTO {table_name} (url, status_code, response_time, check_string, regex_match)
                   VALUES ('{url}','{status_code}', '{response_time}', '{check_string}', '{regex_match}'); """.format(
            table_name=SiteMonitoring.TABLE_NAME,
            url=url,
            status_code=status_code,
            response_time=response_time,
            check_string=check_string,
            regex_match=regex_match)

        cursor, con = self._execute_sql(query)
        cursor.close()
        con.close()

    def check_table_exists(self):
        query = """SELECT * FROM information_schema.tables
                    WHERE table_name = '{table_name}'""".format(table_name=SiteMonitoring.TABLE_NAME)


        cursor, con = self._execute_sql(query)
        res = bool(cursor.rowcount)
        cursor.close()
        con.close()
        return res

    def drop_table(self):
        query = """DROP TABLE {table_name};""".format(table_name=SiteMonitoring.TABLE_NAME)
        cursor, con = self._execute_sql(query)
        cursor.close()
        con.close()

    def get_records(self):
        query = """select * from {table_name}""".format(table_name=SiteMonitoring.TABLE_NAME)
        cursor, con = self._execute_sql(query)
        res = cursor.fetchall()
        cursor.close()
        con.close()
        return res