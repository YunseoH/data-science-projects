# Google Scholar Scraper 📚🔍  

This project is a **Python package for scraping and analyzing Google Scholar data**. It extracts **author profiles, publication details, citation networks**, and stores them in a structured **SQLite database** for further analysis.  

## **Features**
- **Extract Author Profiles**: Retrieves author names, affiliations, h-index, and citation counts.
- **Retrieve Publications**: Collects publication titles, venues, citations, and co-authors.
- **Web Crawling**: `GoogleScholarCrawler.py` **automates navigation through Google Scholar pages** and handles pagination.
- **Data Parsing**: `GoogleScholarParser.py` **extracts structured information** from raw HTML responses.
- **Database Storage & Management**:
  - Stores extracted data in **SQLite** via `GoogleScholarDB.py`.
  - `GoogleScholarDBBuilder.py` **automates database population**.
  - `get_h_index(author_id)`: Calculates an author’s **h-index** from stored publications.
  - `get_citation_graph()`: Generates a **citation network graph** from stored data.
- **Caching System**:
  - `GoogleScholarCacheSQLite.py` and `GoogleScholarCacheFile.py` **store scraped web pages** to avoid redundant requests.
- **Error Handling & Logging**:
  - `GSError.py` defines **custom exceptions** for handling scraping errors.
  - `logger.py` configures **logging** for debugging and tracking performance.
- **Modular Design**:
  - **`scraping/`**: Contains the **core scraper logic**.
  - **`crawler/`**: Manages **web requests and handles pagination**.
  - **`parser/`**: Extracts **structured data from raw HTML**.
  - **`db/`**: Manages **database interactions and schema creation**.
  - **`utils/`**: Contains **helper functions for logging, error handling, and caching**.
