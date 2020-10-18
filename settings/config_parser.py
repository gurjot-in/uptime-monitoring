"""Load configuration from .ini file."""
import configparser


# Read local file `config.ini`.
config = configparser.ConfigParser()
config.read('settings/config.ini')
kafka_config = dict(config.items('KAFKA'))
postgres_config = dict(config.items('POSTGRES'))
monitoring_config = dict(config.items('MONITORING'))