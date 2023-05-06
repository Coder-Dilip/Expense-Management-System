import json
import requests
API_URL = "https://api-inference.huggingface.co/models/gpt2"
API_TOKEN="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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
data = print(query('what do you think why i am so bad in studying?'))
