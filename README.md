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

Repo trail now also keeps:
- `archive/monthly_runs/` for the month by month crawl trail
- `archive/paper_library/` for the pdf files stored once
- `papers/quarterly/` for the quarter summary writeups
- `papers/final_review/` for the all-years review paper

Still not super clean:
- scholar html keeps changing so there are a lot of fallback branches
- archived pages are different from live pages
- works better when the result has a direct pdf link
