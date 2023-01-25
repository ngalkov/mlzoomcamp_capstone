import requests
import json
import sys


url = sys.argv[1]
# url = "http://localhost:3000/predict"

with open('./tests/sample.json') as fp:
    sample = json.load(fp)

result = requests.post(url, json=sample).json()

print(json.dumps(result))