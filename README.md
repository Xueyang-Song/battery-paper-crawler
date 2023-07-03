# znion_ml_paper_crawler

Small hobby crawler for google scholar battery + ml topics.

Main:

```bash
python crawler.py "zinc ion battery machine learning" --limit 2
python crawler.py "zinc ion battery machine learning" --limit 2 --htmlfile fixtures\znion_query_page.html
```

Monthly:

```bat
run_monthly.bat
```

Notes:
- older saved pages and newer result boxes do not look exactly the same
- still doing mostly best effort pdf download
- helper file exists now but it is not very clean
