import requests

query = "zinc ion battery machine learning"
url = "https://scholar.google.com/scholar?q=" + query.replace(" ", "+")
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url headers=headers)
print(response.text[:200])
