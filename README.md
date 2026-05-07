# Battery Paper Crawler

Lightweight Google Scholar harvesting utility for battery and electrochemistry literature workflows, with a focus on PDF-first collection and reproducible run logs.

## Purpose

This repository supports recurring literature collection by:

- querying Google Scholar with battery-domain keywords
- extracting result metadata and candidate PDF links
- downloading reachable PDFs
- writing structured run records for monthly/quarterly review pipelines

It is intended for small, controlled collection runs rather than large-scale crawling.

## Features

- **CLI-driven query runs** (`crawler.py`)
- **Live mode** (request Scholar directly) and **offline fixture mode** (parse saved HTML)
- **Multiple HTML fallback parsers** for different Scholar result layouts
- **Per-run provenance** via `run_info.json` (query, source type, links, statuses, saved files)
- **Simple archive-friendly output tree** under query-specific folders

## Repository layout

```text
.
├── crawler.py                 # main CLI entrypoint
├── scholar_helpers.py         # parser helpers and extraction utilities
├── requirements.txt
├── fixtures/                  # saved Scholar HTML and helper test inputs
├── archive/                   # monthly run trail and paper library snapshots
├── papers/                    # quarterly/final writeups
├── run_monthly.bat            # minimal scheduled runner
└── notes.txt                  # operational notes and historical run trail
```

## Installation

```bash
python3 -m pip install -r requirements.txt
```

## Usage

### 1) Live query run

```bash
python3 crawler.py "zinc ion battery machine learning" --limit 2
```

### 2) Offline parse run (recommended for parser debugging)

```bash
python3 crawler.py "zinc ion battery machine learning" --limit 2 --htmlfile fixtures/znion_query_page.html
```

### 3) Custom output root

```bash
python3 crawler.py "zinc ion battery machine learning" --limit 2 --out-root /tmp/battery-crawler-downloads
```

### 4) Monthly batch entrypoint (Windows)

```bat
run_monthly.bat
```

## Output format

For each query, the crawler creates:

- `<out-root>/<slug-query>/search_page.html` (live mode only)
- `<out-root>/<slug-query>/*.pdf` (downloaded documents)
- `<out-root>/<slug-query>/run_info.json`

`run_info.json` contains:

- query and source metadata (`source_type`, `source_value`)
- list of saved file paths
- per-result extraction records (`kind`, title, links, meta/snippet, save status)
- timestamp of the run

## Parser behavior and limitations

- Google Scholar markup changes frequently; parser logic includes multiple fallback branches.
- Archived/saved Scholar pages can differ structurally from live pages.
- Successful download rates are highest when Scholar exposes direct PDF links.
- Some results are expected to return `not_pdf`, `no_link`, or non-200 statuses.

## Operational guidance

- Keep request rates low and use conservative limits for live runs.
- Prefer fixture-based debugging (`--htmlfile`) when modifying parser logic.
- Treat this tool as a personal research helper, not a high-throughput crawler.
