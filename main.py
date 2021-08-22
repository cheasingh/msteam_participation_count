from msteam import user_score
from airtable import to_airtable

for key, value in user_score.items():
    data = {'name': key, 'score': value}
    to_airtable(data)
