import requests
from bs4 import BeautifulSoup

query = "zinc ion battery machine learning"
url = "https://scholar.google.com/scholar?q=" + query.replace(" ", "+")
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

boxes = soup.find_all("div", {"class": "gs_r"})
print("found", len(boxes))
for box in boxes:
    print(box.get_text()[:80])
