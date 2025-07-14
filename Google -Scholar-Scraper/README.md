# Google Scholar API Package 📚🔍

This is a Python package for **scraping, storing, and analyzing Google Scholar data**.  
It supports fetching author/publication details, computing H-Index, and visualizing citation graphs.

---

## Features
- **Scraping**: Retrieve author and publication data from Google Scholar.
- **Database**: Store parsed data in SQLite for efficient reuse and querying.
- **Analytics**: Compute metrics like **H-Index** and visualize citation graphs using NetworkX.
- **Testing**: Comprehensive unit tests to ensure reliability.

---

## Project Structure
```
├── gscholar/ # Core Python package
│ ├── db/ # Database-related modules (e.g., schema, helpers)
│ ├── scraping/ # Web scraping logic for Google Scholar
│ ├── utils/ # Utility functions (helpers, shared tools)
│ │   ├── GoogleScholarDB.py # Main DB management (create, query, compute H-index)
│ │   └── init.py # Package init
├── test/ # Unit tests for different modules
├── LICENSE # License information
├── scraper.ipynb # Example Jupyter notebook (usage demo & visualization)
├── setup.cfg # Package configuration (metadata)
├── setup.py # Install script for pip install
└── tox.ini # Testing automation config (via tox)
```

---

## Installation

```
pip install .
```
or for development
```
pip install -e .
```

### Example Usuage

```
from gscholar.scraping.GoogleScholar import GoogleScholar
from gscholar.utils.GoogleScholarDB import GoogleScholarDB

gs = GoogleScholar()
author = gs.get_author_details("yySZFKoAAAAJ")

db = GoogleScholarDB("scholar.sqlite")
db.add_author("yySZFKoAAAAJ", "Bruno Bodin")
h_index = db.get_h_index("yySZFKoAAAAJ")
print(f"H-Index: {h_index}")
```
See scraper.ipynb for more advanced examples.

