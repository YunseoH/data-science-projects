# Google Scholar API Package 📚🔍  

## Project Overview
This package provides tools to scrape, store, and analyze author and publication data from **Google Scholar**. It includes:
- Web scraping for Google Scholar author and publication pages.
- Database storage for parsed data.
- Utility functions to compute **H-Index** and visualize citation graphs.

## Project Structure
- **`gscholar/`** - Core package for scraping and database management.
- **`tests/`** - Unit tests for different components.
- **`scraper.ipynb`** - Jupyter Notebook demonstrating package usage.
- **`setup.py` / `setup.cfg`** - Package setup.


## Features
### 1. Scraping Google Scholar Data
```python
from gscholar.scraping.GoogleScholar import GoogleScholar
from gscholar.scraping.cache.GoogleScholarCacheSQLite import GoogleScholarCacheSQLite

db_cache = GoogleScholarCacheSQLite("cache.sqlite")
gs = GoogleScholar(cache=db_cache)

author_id = "yySZFKoAAAAJ"
author_details = gs.get_author_details(author_id)
print(author_details)
```

### 2. Storing and Querying Data
```python
from gscholar.GoogleScholarDB import GoogleScholarDB
db = GoogleScholarDB("scholar_data.sqlite")
db.add_author("yySZFKoAAAAJ", "Bruno Bodin")
```

### 3. Computing H-Index
```python
h_index = db.get_h_index("yySZFKoAAAAJ")
print(f"H-Index: {h_index}")
```

### 4. Citation Graph Visualization
```python
import networkx as nx
graph = db.get_citation_graph()
nx.draw(graph, node_size=100, with_labels=True)
```

## 🛠 Running Tests
Run the full test suite using:
```sh
tox
```
Example output:
```sh
============================================= test session starts =============================================
collected 28 items

tests/test_GSCacheCopy.py ..     [  7%]
tests/test_GSCrawler.py .        [ 10%]
tests/test_GSDB.py ......        [ 32%]
tests/test_GSDBBuilder.py ....   [ 46%]
tests/test_GoogleScholarCache.py ........   [ 89%]
tests/test_GoogleScholarParser.py ...   [100%]

======================================= 24 passed, 4 skipped =======================================
```
