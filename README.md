# 📚 MarketScraper — Competitive Pricing Intelligence ETL Pipeline

> **Domain:** Publishing & Market Intelligence | **Category:** Web Scraping · Data Engineering · OOP  
> **Stack:** Python · Requests · BeautifulSoup4 · Pandas

---

## 💡 Project Overview

I built this ETL pipeline as a hands-on data engineering project to simulate a **real-world competitive analysis workflow**.

**The Business Problem it solves:** Imagine a publishing house that needs to understand how competitors price and rate their Mystery titles — manually browsing hundreds of pages isn't scalable. This pipeline automates the entire process: it systematically extracts product data from ["Books to Scrape"](https://books.toscrape.com) (a publicly available sandbox catalogue built for exactly this kind of practice), transforms it into a clean, structured format, and loads it into a CSV ready for analysis.

**Key Business Questions This Dataset Can Answer:**
- What is the going price range for Mystery genre titles?
- How do customer ratings distribute across price points?
- Which titles are in stock and at what price point — and where are the gaps?

---

## ⚙️ Technical Architecture — The ETL Pipeline

This project implements a full **Extract → Transform → Load (ETL)** pipeline, encapsulated within a single Object-Oriented `MarketScraper` class.

```
┌─────────────────────────────────────────────────────────┐
│                    MarketScraper OOP Class              │
│                                                         │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ EXTRACT  │ →  │  TRANSFORM   │ →  │     LOAD      │  │
│  │          │    │              │    │               │  │
│  │ requests │    │ Rating map   │    │ pandas        │  │
│  │ BS4 parse│    │ String clean │    │ DataFrame     │  │
│  │ Paginate │    │ Dict struct  │    │ CSV export    │  │
│  └──────────┘    └──────────────┘    └───────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔒 Failsafe Architecture — Dynamic Pagination

One of the core engineering decisions in this project is the **HTTP 200 OK pagination failsafe**. Instead of hardcoding the number of pages (brittle) or pre-crawling a sitemap (expensive), the scraper:

1. Constructs page URLs dynamically: `/page-{n}.html`
2. Sends a `GET` request and **inspects the HTTP status code**
3. Continues scraping only while `status_code == 200`
4. Gracefully terminates and logs the exit point upon receiving any non-200 response (e.g., `404 Not Found`)

```python
while True:
    target_url = f"{start_url}/page-{num}.html"
    r = requests.get(target_url)

    if r.status_code != 200:
        print(f"Target exhausted. Scraping completed at page {num - 1}.")
        break
    # ... process page
    num += 1
```

**Why this matters:** This makes the scraper **self-terminating and resilient** — it adapts automatically to catalogues of any size without manual intervention.

---

## 🔄 Data Transformation Logic

### 1. Textual Rating → Integer Mapping
The source HTML encodes star ratings as CSS class names (e.g., `class="star-rating Three"`). A dictionary map converts these to usable integers:

```python
self.mapping_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
```

### 2. String Cleaning
Availability status text is stripped of surrounding whitespace via `.text.strip()` to ensure clean, consistent values in the output dataset.

### 3. Structured Output Per Record
Each book is extracted into a clean Python dictionary before being appended to the master list:

| Field | Source | Transformation |
|---|---|---|
| `Title` | `<a title="...">` | Direct attribute extraction |
| `Price` | `.price_color` class | Direct text extraction |
| `Ratings` | `.star-rating` CSS class | Dictionary mapping → integer |
| `Availability Status` | `.instock.availability` class | `.strip()` whitespace cleaning |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `Python 3.x` | Core language |
| `requests` | HTTP GET requests & status code validation |
| `BeautifulSoup4` | HTML parsing & DOM traversal |
| `pandas` | DataFrame construction & CSV export |

---

## 🚀 Usage

```python
# 1. Instantiate the scraper
scraper = MarketScraper()

# 2. Run the full scraping pipeline on the Mystery category
scraper.scrape_category("https://books.toscrape.com/catalogue/category/books/mystery_3")

# 3. Export results to CSV and retrieve the DataFrame
final_df = scraper.export_to_csv("mystery_competitors.csv")

# 4. Inspect results
print(final_df.head())
```

**Expected Output:**
```
Initiating scraping protocol for: https://...mystery_3...
Successfully breached page 1...
Successfully breached page 2...
Target exhausted. Scraping completed at page 2.
SUCCESS: Exported 32 rows to mystery_competitors.csv.
```

---

## 📊 Sample Output (mystery_competitors.csv)

| Title | Price | Ratings | Availability Status |
|---|---|---|---|
| Sharp Objects | £47.82 | 4 | In stock |
| In a Dark, Dark Wood | £19.63 | 1 | In stock |
| The Past Never Ends | £56.50 | 4 | In stock |
| ... | ... | ... | ... |

---

## 🧠 Key Engineering Decisions & Lessons

- **OOP Encapsulation:** Wrapping the scraper in a class allows `master_list` and `mapping_dict` to persist across method calls, making the architecture modular and extensible.
- **Separation of Concerns:** `extract_book_data()` handles a single record; `scrape_category()` handles pagination; `export_to_csv()` handles output — each method has one job.
- **Fail Fast, Exit Clean:** The `status_code != 200` gate means the scraper never silently processes empty or error pages.

---

## 📁 Repository Structure

```
markscraper/
│
├── market_scraper.py        # Main scraper class (ETL pipeline)
├── mystery_competitors.csv  # Output dataset
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---
