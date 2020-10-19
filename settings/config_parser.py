"""Load configuration from config.yaml file."""
import yaml

with open("settings/conf.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

postgres = config.get('postgres')
kafka = config.get('kafka')
sites = config.get('websites')

print(sites)