# znion_ml_paper_crawler

Hobby google scholar crawler for machine learning + battery paper hunting.

Main:

```bash
python crawler.py "zinc ion battery machine learning" --limit 2
python crawler.py "zinc ion battery machine learning" --limit 2 --htmlfile fixtures\znion_query_page.html
python crawler.py "zinc ion battery machine learning" --limit 2 --out-root E:\somewhere\else
```

Monthly:

```bat
run_monthly.bat
```

It saves pdfs under `downloads/<query-slug>/` and now also writes a simple `run_info.json`.
The repo also keeps the crawl archive under `archive/` and the writeups under `papers/`.

Things that are still not great:
- scholar html keeps changing so there are a lot of fallback branches
- archived pages are different from live pages
- works better when the result has a direct pdf link
