import os
import sys
import requests
from bs4 import BeautifulSoup

query = " ".join(sys.argv[1:])
search_text = query + " filetype:pdf"
url = "https://scholar.google.com/scholar?q=" + search_text.replace(" ", "+")
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

if not os.path.exists("downloads"):
    os.mkdir("downloads")

boxes = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})
for box in boxes:
    side = box.find("div", {"class": "gs_or_ggsm"})
    if not side:
        continue
    a = side.find("a")
    if not a:
        continue
    pdf = requests.get(a.get("href"))
    name = a.get("href").split("/")[-1]
    out = open(os.path.join("downloads", name), "wb")
    out.write(pdf.content)
    out.close()
    print("saved", name)
