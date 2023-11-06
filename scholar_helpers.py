import json
import os


def slug_text(text):
    out = text.lower().strip()
    out = out.replace("/", "_")
    out = out.replace("\\", "_")
    out = out.replace(" ", "_")
    while "__" in out:
        out = out.replace("__", "_")
    return out


def clean_title(text):
    text = text.replace("[PDF] ", "")
    text = text.replace("[CITATION] ", "")
    text = text.replace("[C] ", "")
    text = text.replace("[引用] ", "")
    return text.strip()


def unwrap_archive_link(url):
    if "/https://" in url:
        return "https://" + url.split("/https://", 1)[1]
    if "/http://" in url:
        return "http://" + url.split("/http://", 1)[1]
    return url


def collect_boxes(soup):
    boxes = []
    for box in soup.find_all("div", {"class": "gs_r gs_or gs_scl"}):
        boxes.append(("classic", box))
    if boxes:
        return boxes
    for box in soup.find_all("div", {"class": "gs_ri"}):
        boxes.append(("direct_ri", box))
    if boxes:
        return boxes
    for box in soup.find_all("div", attrs={"data-rp": True}):
        if box.find("h3"):
            boxes.append(("data_rp", box))
    if boxes:
        return boxes
    return boxes


def pick_info_and_side(kind, box):
    if kind == "classic":
        return box.find("div", {"class": "gs_ri"}), box.find("div", {"class": "gs_or_ggsm"})
    if kind == "data_rp":
        return box.find("div", {"class": "gs_ri"}) or box, box.find("div", {"class": "gs_or_ggsm"})
    return box, None


def find_pdf_link(kind, box, side):
    if side and side.find("a"):
        return side.find("a").get("href", "")
    if kind == "archive_old":
        for part in box.find_all("div", recursive=False)[:2]:
            for a in part.find_all("a"):
                href = a.get("href", "")
                text = a.get_text(" ", strip=True).lower()
                if text.startswith("[pdf]") or ".pdf" in href.lower() or "download" in href.lower():
                    return href
    return ""


def extract_result(kind, box):
    info, side = pick_info_and_side(kind, box)
    if not info:
        return None
    h3 = info.find("h3")
    if not h3:
        return None
    title = clean_title(h3.get_text(" ", strip=True))
    a = h3.find("a")
    main_link = a.get("href", "") if a else ""
    meta = ""
    snippet = ""
    meta_box = info.find("div", {"class": "gs_a"})
    if meta_box:
        meta = meta_box.get_text(" ", strip=True)
    snippet_box = info.find("div", {"class": "gs_rs"})
    if snippet_box:
        snippet = snippet_box.get_text(" ", strip=True)
    pdf_link = find_pdf_link(kind, box, side)
    return {
        "kind": kind,
        "title": title,
        "main_link": unwrap_archive_link(main_link),
        "pdf_link": unwrap_archive_link(pdf_link),
        "meta": meta,
        "snippet": snippet,
    }
