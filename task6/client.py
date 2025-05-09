# curl "http://127.0.0.1:8000/primes?limit=100"

import requests

response = requests.get("http://127.0.0.1:8000/primes", params={"limit": 100})
print(response.json())