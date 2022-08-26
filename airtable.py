from posixpath import dirname
from pyairtable import Table
from pyairtable.formulas import match
from dotenv import load_dotenv
from os.path import join, dirname
from os import environ
from msteam import get_member

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
        table.create({'Name': name, 'MS Team Q/A': value, 'Class Practice': 0})
    else:
        # update if the value is different from the one online
        if record['fields']['MS Team Q/A'] != value:
            table.update(record['id'], {"MS Team Q/A": value})


def add_class_participation(data):
    name, value = data.values()

    member_display_name = get_member(name)

    # member found on msteam
    if member_display_name:

        verify = match({"Name": member_display_name})
        record = table.first(formula=verify)

        if record == None:
            # if the member is new to airtable
            # create new record with ms team q/a value 0
            table.create({'Name': member_display_name, 'MS Team Q/A': 0,
                          'Class Practice': value})

            print(f'created, {member_display_name} score={value}')

        else:
            # if the member is already on airtable
            # update if the value is different from the one online
            update_score = record['fields']['Class Practice'] + value
            table.update(record['id'], {"Class Practice": update_score})

            print(
                f'update {member_display_name} score from {record["fields"]["Class Practice"]} to {update_score}')

    else:
        print('student not found!')
