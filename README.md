# Product Parser

**Author: YohanDev**

Python script for automated product data collection from online stores.

---

## Features

- ✅ Parse product listings (title, price, rating, stock)
- ✅ Multi-page support
- ✅ Export to CSV
- ✅ Statistics & analytics
- ✅ Find best deals (filter by price/rating)
- ✅ Polite scraping (delays between requests)
- ✅ Error handling

---

## Installation

```bash
pip install requests beautifulsoup4
```

---

## Usage

**Basic usage:**
```bash
python product_parser.py
```

**Custom usage in your code:**
```python
from product_parser import ProductParser

parser = ProductParser()
parser.parse_multiple_pages(num_pages=5)
parser.get_statistics()
parser.save_to_csv("my_products.csv")
```

---

## Output Example

```
============================================================
  PRODUCT PARSER by YohanDev
============================================================

[START] Parsing 3 pages from https://books.toscrape.com

[INFO] Parsing page 1...
  ✓ A Light in the Attic... — £51.77 — ★★★
  ✓ Tipping the Velvet... — £53.74 — ★
  ✓ Soumission... — £50.10 — ★
  ...

[DONE] Total products collected: 60

============================================================
  STATISTICS
============================================================
  Total products:    60
  In stock:          60
  Average price:     £35.64
  Price range:       £10.00 — £59.99
  Average rating:    ★★★ (3.0/5)
============================================================

[SAVED] Data exported to: products_20250101_120000.csv
```

---

## CSV Output Format

| title | price | price_value | rating | in_stock | url | image_url | parsed_at |
|-------|-------|-------------|--------|----------|-----|-----------|-----------|
| Product Name | £29.99 | 29.99 | 4 | True | https://... | https://... | 2025-01-01 12:00:00 |

---

## Customization

**Parse more pages:**
```python
parser.parse_multiple_pages(num_pages=10)
```

**Find deals with custom filters:**
```python
parser.find_best_deals(max_price=25, min_rating=3)
```

---

## Legal Note

This parser is designed for educational purposes and demonstration. 
Always check website's robots.txt and Terms of Service before scraping.

---

## Contact

**YohanDev** — Code & Automation
