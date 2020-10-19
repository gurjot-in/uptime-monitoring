
# Uptime Monitoring

Website availability checker using fully managed kafka and postgres services.

## Installation

[Python 3.7](https://www.python.org/downloads/release/python-370/)  is required

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

## Configuration

 - Create a new kafka topic in Aiven console
 - Edit configuration file and keys in `settings/conf.yaml` as per your service account

## Usage

```bash
python producer.py
python consumer.py 
```

## To Do

 - [ ] Mock unit tests

## References

 - https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka
 - https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql
 - https://stackoverflow.com/questions/17044259/python-how-to-check-if-table-exists/17044893
 - https://github.com/aiven/aiven-examples

## License
[MIT](https://choosealicense.com/licenses/mit/)
