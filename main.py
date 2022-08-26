from msteam import msteam_qa_update
from airtable import to_airtable

user_score = msteam_qa_update()

for key, value in user_score.items():
    data = {'name': key, 'score': value}
    to_airtable(data)
