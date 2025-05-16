# Crawl Archive

This folder keeps the month by month scholar crawl trail inside the same repo.

What is here:
- `monthly_runs/YYYY-MM/<query>/` keeps a normalized manifest and the search result metadata for that month
- `paper_library/` stores each unique pdf only once, even if the same paper showed up again in later months

Range right now:
- first month: `2022-06`
- latest month: `2025-05`
- unique pdf files in library: `101`

Note:
- the first few 2022 months were backfilled once the crawler stopped breaking enough to save things
- repeated monthly recrawls point back into the shared pdf library instead of copying the same file over and over
