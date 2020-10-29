import requests
import json


r = requests.delete(
    'http://127.0.0.1:8000/files',
    data=json.dumps({'hash': 'ec4c2a53be64754d36e9dc19831c439e8f7e342ef941f52db1664308'})
)

print(r.status_code)
print(r.content)

