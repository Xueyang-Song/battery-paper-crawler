# znion_ml_paper_crawler

Finding papers from google scholar about Zinc ion battery / battery / machine learning.

Run once a month and get me updated.

Main:

```bash
python crawler.py "zinc ion battery machine learning" --limit 2
```

If you already saved a scholar page:

```bash
python crawler.py "zinc ion battery machine learning" --limit 2 --htmlfile fixtures\znion_query_page.html
```

It saves pdfs into `downloads/<query>/`.

Problems:
- still likes direct pdf links best
- scholar blocks sometimes
- titles make ugly file names
