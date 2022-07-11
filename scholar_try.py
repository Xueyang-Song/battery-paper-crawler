import sys
import requests
from bs4 import BeautifulSoup

query = " ".join(sys.argv[1:])
search_text = query + " filetype:pdf"
url = "https://scholar.google.com/scholar?q=" + search_text.replace(" ", "+")
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

boxes = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})
for box in boxes:
    title = box.find("h3")
    if title:
        print(title.get_text(" ", strip=True))
