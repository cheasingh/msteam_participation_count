from posixpath import dirname
from pyairtable import Table
from pyairtable.formulas import match
from dotenv import load_dotenv
from os.path import join, dirname
from os import environ

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# document
# https://pyairtable.readthedocs.io/en/latest/api.html#creating-records

airtable_api = environ.get("AIRTABLE_API")
airtable_base = environ.get("AIRTABLE_BASE")
airtable_table = environ.get("AIRTABLE_TABLE")

table = Table(airtable_api, airtable_base, airtable_table)


def to_airtable(data):
    name, value = data.values()
    verify = match({"Name": name})

    # check if data is exist
    record = table.first(formula=verify)

    if record == None:
        # create new record
        table.create({'Name': name, 'MS Team Q/A': value})
    else:
        # update if the value is different from the one online
        if record['fields']['MS Team Q/A'] != value:
            table.update(record['id'], {"MS Team Q/A": value})
