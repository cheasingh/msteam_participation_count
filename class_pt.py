from airtable import add_class_participation
from msteam import get_member

while True:
    name = input("student name/email/id: ")

    display_name = get_member(name)

    if display_name:
        print(f"student found: {display_name}")
        score = int(input("score: "))

        data = {'name': name, 'value': score}
        add_class_participation(data)
    else:
        print("student not found!")
