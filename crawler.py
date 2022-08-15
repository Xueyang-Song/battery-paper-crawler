import os
import sys
import time
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0 Safari/537.36"
}

limit = 3
htmlfile = ""
query_parts = []
i = 1
while i < len(sys.argv):
    if sys.argv[i] == "--limit":
        limit = int(sys.argv[i + 1])
        i = i + 2
    elif sys.argv[i] == "--htmlfile":
        htmlfile = sys.argv[i + 1]
        i = i + 2
    else:
        query_parts.append(sys.argv[i])
        i = i + 1

if len(query_parts) == 0:
    print("put search words")
    sys.exit()

query = " ".join(query_parts)
search_text = query + " filetype:pdf"
folder_name = query.replace(" ", "_")

if not os.path.exists("downloads"):
    os.mkdir("downloads")
if not os.path.exists(os.path.join("downloads", folder_name)):
    os.mkdir(os.path.join("downloads", folder_name))

if htmlfile:
    f = open(htmlfile, "r", encoding="utf-8")
    html = f.read()
    f.close()
else:
    scholar_url = "https://scholar.google.com/scholar?q=" + search_text.replace(" ", "+")
    response = requests.get(scholar_url, headers=headers, timeout=25)
    html = response.text

soup = BeautifulSoup(html, "html.parser")
wraps = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})
done = 0

for wrap in wraps:
    if done >= limit:
        break
    try:
        info = wrap.find("div", {"class": "gs_ri"})
        side = wrap.find("div", {"class": "gs_or_ggsm"})
        if not info:
            continue
        h3 = info.find("h3")
        if not h3:
            continue
        title = h3.get_text(" ", strip=True)
        print("title", title)
        a = h3.find("a")
        link = ""
        if side and side.find("a"):
            link = side.find("a").get("href", "")
        elif a:
            link = a.get("href", "")
        if link == "":
            continue
        pdf_r = requests.get(link, headers=headers, timeout=25)
        if pdf_r.status_code != 200:
            continue
        name = title[:80].replace("/", "_")
        out = open(os.path.join("downloads", folder_name, name + ".pdf"), "wb")
        out.write(pdf_r.content)
        out.close()
        done = done + 1
        time.sleep(2)
    except Exception as e:
        print("one result failed", e)
