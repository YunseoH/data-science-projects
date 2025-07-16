# Google Scholar Scraper 🔍

This project was developed as part of a university assignment to build a complete data pipeline for extracting and analyzing academic metrics from Google Scholar.  
It combines automated scraping, intelligent caching, structured storage, and simple network analysis to explore author profiles and citation relationships.

---

## What it does
- 🔎 **Scrapes Google Scholar:**  
  Collects author profiles (name, affiliation, citations, h-index, i10-index), publication lists, and citation links using Selenium + BeautifulSoup.

- 💾 **Caches fetched pages:**  
  Efficient caching to avoid redundant requests, with support for both file-based (`GoogleScholarCacheFile`) and SQLite-based (`GoogleScholarCacheSQLite`) backends.

- 🗄️ **Builds structured database:**  
  Stores data in a relational SQLite DB with tables for authors, publications, authorship, and citation edges.

- 📈 **Analyzes academic networks:**  
  - `get_h_index(author_id)`: computes H-index directly via SQL queries.
  - `get_citation_graph(focus_authors=None)`: creates a citation network using NetworkX (or pyvis for interactive HTML).

---

## Key Features
- **DB Builder:**  
  Use `GoogleScholarDBBuilder` to populate the database in bulk by fetching multiple authors and their entire citation graph.

- **Cache merging:**  
  `copy_into()` allows merging caches from different runs or storage types.

- **Visualization:**  
  Quickly plot citation networks, highlight influential papers, or export interactive HTML graphs.

---

## Example Usage
```python
from gscholar.scraping.GoogleScholar import GoogleScholar
from gscholar.scraping.cache.GoogleScholarCacheSQLite import GoogleScholarCacheSQLite
from gscholar.GoogleScholarDB import GoogleScholarDB
from gscholar.db.GoogleScholarDBBuilder import GoogleScholarDBBuilder

# Setup
cache = GoogleScholarCacheSQLite("my_cache.sqlite")
gs = GoogleScholar(cache=cache)
db = GoogleScholarDB("my_academic_data.sqlite")
builder = GoogleScholarDBBuilder(gs, db)

# Fetch authors and build database
author_list = ["1TUANHcAAAAJ", "x2MfRUYAAAAJ", "ky6n3gwAAAAJ"]
builder.fetch_authors(author_list)

# Analysis
print(db.get_h_index("1TUANHcAAAAJ"))
graph = db.get_citation_graph(focus_authors=author_list)

# Visualization with NetworkX
import networkx as nx
import matplotlib.pyplot as plt
nx.draw(graph, with_labels=True, node_size=50)
plt.show()
```

## Technologies
- Python (Selenium, BeautifulSoup, SQLite, pandas, networkx, pyvis)
- SQL for direct H-index computation
