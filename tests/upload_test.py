import requests


with open('cat.jpg', 'rb') as f:
    r = requests.put('http://127.0.0.1:8000/files', files={'cat.jpg': f})

print(r.status_code)
print(r.content)
