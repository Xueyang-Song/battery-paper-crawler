import os
import sys
import time
import requests
from bs4 import BeautifulSoup

query = " ".join(sys.argv[1:])
search_text = query + " filetype:pdf"
url = "https://scholar.google.com/scholar?q=" + search_text.replace(" ", "+")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0 Safari/537.36"
}

if not os.path.exists("downloads"):
    os.mkdir("downloads")

response = requests.get(url, headers=headers, timeout=20)
soup = BeautifulSoup(response.text, "html.parser")

boxes = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})
for box in boxes:
    try:
        side = box.find("div", {"class": "gs_or_ggsm"})
        if not side:
            continue
        a = side.find("a")
        if not a:
            continue
        link = a.get("href", "")
        if link == "":
            continue
        pdf = requests.get(link, headers=headers, timeout=20)
        if pdf.status_code != 200:
            continue
        name = link.split("/")[-1]
        if "." not in name:
            name = "paper_" + str(int(time.time())) + ".pdf"
        out = open(os.path.join("downloads", name), "wb")
        out.write(pdf.content)
        out.close()
        print("saved", name)
        time.sleep(2)
    except Exception as e:
        print("one failed", e)
