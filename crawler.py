import os
import sys
import time
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
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
folder_name = query.replace(" ", "_").replace("/", "_")

if not os.path.exists("downloads"):
    os.mkdir("downloads")
if not os.path.exists(os.path.join("downloads", folder_name)):
    os.mkdir(os.path.join("downloads", folder_name))

if htmlfile:
    print("using html file", htmlfile)
    with open(htmlfile, "r", encoding="utf-8") as handle:
        html = handle.read()
else:
    scholar_url = "https://scholar.google.com/scholar?q=" + quote_plus(search_text)
    print("getting scholar page")
    print(scholar_url)
    response = requests.get(scholar_url, headers=headers, timeout=25)
    print("status", response.status_code)
    if response.status_code != 200:
        print("scholar did not work")
        sys.exit()
    html = response.text


soup = BeautifulSoup(html, "html.parser")
wraps = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})
if len(wraps) == 0:
    wraps = soup.find_all("div", {"class": "gs_ri"})

print("results found", len(wraps))
done = 0

for wrap in wraps:
    if done >= limit:
        break
    try:
        if wrap.get("class") and "gs_ri" in wrap.get("class"):
            info = wrap
            side = None
        else:
            info = wrap.find("div", {"class": "gs_ri"})
            side = wrap.find("div", {"class": "gs_or_ggsm"})
        if not info:
            continue
        h3 = info.find("h3")
        if not h3:
            continue
        title = h3.get_text(" ", strip=True).replace("[PDF] ", "")
        print("title", title)
        a = h3.find("a")
        use_link = ""
        if side and side.find("a"):
            use_link = side.find("a").get("href", "")
        elif a:
            use_link = a.get("href", "")
        if use_link == "":
            continue
        pdf_r = requests.get(use_link, headers=headers, timeout=25)
        ctype = pdf_r.headers.get("content-type", "").lower()
        if pdf_r.status_code != 200:
            continue
        if ".pdf" not in use_link.lower() and "pdf" not in ctype:
            continue
        name = title[:80]
        for bad in '\\/:*?"<>|':
            name = name.replace(bad, "_")
        out_path = os.path.join("downloads", folder_name, name + ".pdf")
        with open(out_path, "wb") as out:
            out.write(pdf_r.content)
        print("saved", out_path)
        done = done + 1
        time.sleep(2)
    except Exception as e:
        print("one result failed")
        print(e)

print("done got", done, "pdfs")
