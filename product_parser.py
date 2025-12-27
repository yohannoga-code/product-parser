# Author: YohanDev
# Product Parser — collects product data from website and saves to CSV

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import os

class ProductParser:
    """Parser for collecting product data from online store"""
    
    def __init__(self):
        self.base_url = "https://books.toscrape.com"
        self.products = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def get_page(self, url):
        """Fetch page content"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            return None
    
    def parse_rating(self, rating_class):
        """Convert rating class to number"""
        ratings = {
            "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
        }
        return ratings.get(rating_class, 0)
    
    def parse_product_page(self, url):
        """Parse individual product page for details"""
        soup = self.get_page(url)
        if not soup:
            return None
        
        try:
            # Get product description
            desc_tag = soup.select_one("#product_description ~ p")
            description = desc_tag.text.strip() if desc_tag else "No description"
            
            # Get stock info
            stock_tag = soup.select_one(".availability")
            stock = stock_tag.text.strip() if stock_tag else "Unknown"
            
            # Get UPC (unique product code)
            upc_tag = soup.select_one("table tr:nth-child(1) td")
            upc = upc_tag.text.strip() if upc_tag else "N/A"
            
            return {
                "description": description[:200] + "..." if len(description) > 200 else description,
                "stock": stock,
                "upc": upc
            }
        except Exception as e:
            print(f"[ERROR] Failed to parse product details: {e}")
            return None
    
    def parse_catalog_page(self, page_num=1):
        """Parse catalog page with product listings"""
        if page_num == 1:
            url = f"{self.base_url}/catalogue/page-{page_num}.html"
        else:
            url = f"{self.base_url}/catalogue/page-{page_num}.html"
        
        print(f"\n[INFO] Parsing page {page_num}...")
        soup = self.get_page(url)
        
        if not soup:
            return False
        
        products = soup.select("article.product_pod")
        
        if not products:
            print("[INFO] No more products found")
            return False
        
        for product in products:
            try:
                # Product title
                title_tag = product.select_one("h3 a")
                title = title_tag["title"] if title_tag else "Unknown"
                
                # Product URL
                product_url = self.base_url + "/catalogue/" + title_tag["href"].replace("../", "") if title_tag else None
                
                # Price
                price_tag = product.select_one(".price_color")
                price = price_tag.text.strip() if price_tag else "N/A"
                price_value = float(price.replace("£", "").replace("Â", "")) if price != "N/A" else 0
                
                # Rating
                rating_tag = product.select_one(".star-rating")
                rating_class = rating_tag["class"][1] if rating_tag else "Zero"
                rating = self.parse_rating(rating_class)
                
                # Availability
                stock_tag = product.select_one(".availability")
                in_stock = "In stock" in stock_tag.text if stock_tag else False
                
                # Image URL
                img_tag = product.select_one(".thumbnail img")
                image_url = self.base_url + "/" + img_tag["src"].replace("../", "") if img_tag else None
                
                product_data = {
                    "title": title,
                    "price": price,
                    "price_value": price_value,
                    "rating": rating,
                    "in_stock": in_stock,
                    "url": product_url,
                    "image_url": image_url,
                    "parsed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.products.append(product_data)
                print(f"  ✓ {title[:50]}... — {price} — {'★' * rating}")
                
            except Exception as e:
                print(f"[ERROR] Failed to parse product: {e}")
                continue
        
        return True
    
    def parse_multiple_pages(self, num_pages=3):
        """Parse multiple catalog pages"""
        print("=" * 60)
        print("  PRODUCT PARSER by YohanDev")
        print("=" * 60)
        print(f"\n[START] Parsing {num_pages} pages from {self.base_url}")
        
        for page in range(1, num_pages + 1):
            success = self.parse_catalog_page(page)
            if not success:
                break
            time.sleep(0.5)  # Polite delay between requests
        
        print(f"\n[DONE] Total products collected: {len(self.products)}")
        return self.products
    
    def save_to_csv(self, filename=None):
        """Save parsed data to CSV file"""
        if not self.products:
            print("[WARNING] No products to save")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"products_{timestamp}.csv"
        
        fieldnames = ["title", "price", "price_value", "rating", "in_stock", "url", "image_url", "parsed_at"]
        
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.products)
            
            print(f"\n[SAVED] Data exported to: {filename}")
            return filename
        except Exception as e:
            print(f"[ERROR] Failed to save CSV: {e}")
            return None
    
    def get_statistics(self):
        """Calculate and display statistics"""
        if not self.products:
            return None
        
        prices = [p["price_value"] for p in self.products if p["price_value"] > 0]
        ratings = [p["rating"] for p in self.products]
        in_stock = sum(1 for p in self.products if p["in_stock"])
        
        stats = {
            "total_products": len(self.products),
            "in_stock": in_stock,
            "out_of_stock": len(self.products) - in_stock,
            "avg_price": round(sum(prices) / len(prices), 2) if prices else 0,
            "min_price": min(prices) if prices else 0,
            "max_price": max(prices) if prices else 0,
            "avg_rating": round(sum(ratings) / len(ratings), 1) if ratings else 0
        }
        
        print("\n" + "=" * 60)
        print("  STATISTICS")
        print("=" * 60)
        print(f"  Total products:    {stats['total_products']}")
        print(f"  In stock:          {stats['in_stock']}")
        print(f"  Out of stock:      {stats['out_of_stock']}")
        print(f"  Average price:     £{stats['avg_price']}")
        print(f"  Price range:       £{stats['min_price']} — £{stats['max_price']}")
        print(f"  Average rating:    {'★' * int(stats['avg_rating'])} ({stats['avg_rating']}/5)")
        print("=" * 60)
        
        return stats
    
    def find_best_deals(self, max_price=20, min_rating=4):
        """Find products with good rating and low price"""
        deals = [
            p for p in self.products 
            if p["price_value"] <= max_price 
            and p["rating"] >= min_rating 
            and p["in_stock"]
        ]
        
        if deals:
            print(f"\n[DEALS] Best deals (under £{max_price}, {min_rating}+ stars):")
            for deal in sorted(deals, key=lambda x: x["price_value"])[:5]:
                print(f"  • {deal['title'][:40]}... — {deal['price']} — {'★' * deal['rating']}")
        
        return deals


def main():
    """Main function — run parser"""
    parser = ProductParser()
    
    # Parse 3 pages of products
    parser.parse_multiple_pages(num_pages=3)
    
    # Show statistics
    parser.get_statistics()
    
    # Find best deals
    parser.find_best_deals(max_price=15, min_rating=4)
    
    # Save to CSV
    parser.save_to_csv()
    
    print("\n[COMPLETE] Parser finished successfully!\n")


if __name__ == "__main__":
    main()
