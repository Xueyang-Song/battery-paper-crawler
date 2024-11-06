import argparse
import os
import sys
import time
from datetime import datetime
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from scholar_helpers import collect_boxes, extract_result, slug_text, write_json


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="+")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--htmlfile")
    parser.add_argument("--out-root", default="downloads")
    return parser.parse_args()


def pick_folder(query, args):
    out_root = args.out_root
    os.makedirs(out_root, exist_ok=True)
    folder = os.path.join(out_root, slug_text(query))
    os.makedirs(folder, exist_ok=True)
    return folder


args = build_args()
query = " ".join(args.query).strip()
if query == "":
    print("put search words")
    sys.exit()

folder = pick_folder(query, args)
source_type = "live"
source_value = ""

if args.htmlfile:
    source_type = "htmlfile"
    source_value = args.htmlfile
    print("using html file", args.htmlfile)
    with open(args.htmlfile, "r", encoding="utf-8") as handle:
        html = handle.read()
else:
    search_url = "https://scholar.google.com/scholar?q=" + quote_plus(query + " filetype:pdf")
    source_value = search_url
    print("getting scholar page")
    print(search_url)
    response = requests.get(search_url, headers=headers, timeout=20)
    print("status", response.status_code)
    if response.status_code != 200:
        print("scholar did not work")
        sys.exit()
    html = response.text
    with open(os.path.join(folder, "search_page.html"), "w", encoding="utf-8") as page_out:
        page_out.write(html)

soup = BeautifulSoup(html, "html.parser")
boxes = collect_boxes(soup)
print("results found", len(boxes))
saved_files = []
records = []
done = 0

for kind, box in boxes:
    if done >= args.limit:
        break
    try:
        one = extract_result(kind, box)
        if not one:
            continue
        print("title", one["title"])
        use_link = one["pdf_link"] or one["main_link"]
        if use_link == "":
            one["save_status"] = "no_link"
            records.append(one)
            continue
        print("trying", use_link)
        pdf_r = requests.get(use_link, headers=headers, timeout=20)
        ctype = pdf_r.headers.get("content-type", "").lower()
        if pdf_r.status_code != 200:
            one["save_status"] = "status_" + str(pdf_r.status_code)
            records.append(one)
            continue
        if ".pdf" not in use_link.lower() and "pdf" not in ctype:
            one["save_status"] = "not_pdf"
            records.append(one)
            continue
        name = one["title"][:90] or "paper"
        for bad in '\\/:*?"<>|':
            name = name.replace(bad, "_")
        path = os.path.join(folder, name + ".pdf")
        with open(path, "wb") as out:
            out.write(pdf_r.content)
        print("saved", path)
        one["save_status"] = "saved"
        one["saved_path"] = path
        saved_files.append(path)
        records.append(one)
        done = done + 1
        time.sleep(1)
    except Exception as e:
        print("one result failed")
        print(e)

print("done got", done, "pdfs")
run_info = {
    "query": query,
    "source_type": source_type,
    "source_value": source_value,
    "saved_files": saved_files,
    "results_seen": records,
    "run_time": datetime.now().isoformat(),
}
write_json(os.path.join(folder, "run_info.json"), run_info)
