import requests
from bs4 import BeautifulSoup
import re
import time
import json
import csv
import os
webpage_scraped= input("What webpage would you like to scrape?: ")
def scrape_laptop_page(page_number):
    url = f"{webpage_scraped}&pagenumber={page_number}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        for product in soup.select('.prbox_box.prbox_img'):
            name = product.select_one('.prbox_name').get_text(strip=True) if product.select_one('.prbox_name') else None
            
            product_url = product.select_one('.prbox_link')['href'] if product.select_one('.prbox_link') else None
            if product_url and not product_url.startswith('http'):
                product_url = 'https://www.centrecom.com.au' + product_url
            
            image_data = product.get('data-lazy', '')
            image_url = re.search(r'url\((.*?)\)', image_data).group(1) if image_data else None
            
            features = [li.get_text(strip=True) for li in product.select('.prbox_salespoints ul li')]
            
            sale_price = product.select_one('.saleprice').get_text(strip=True) if product.select_one('.saleprice') else None
            was_price = product.select_one('.wasprice').get_text(strip=True) if product.select_one('.wasprice') else None
            
            stock_icons = {}
            for icon in product.select('.prbox_icon'):
                icon_type = re.search(r'prbox_(green|yellow|red|grey|blue)', ' '.join(icon.get('class', [])))
                icon_type = icon_type.group(1) if icon_type else None
                tooltip = icon.select_one('.tooltip').get_text(strip=True) if icon.select_one('.tooltip') else None
                if icon_type and tooltip:
                    stock_icons[icon_type] = tooltip
            
            products.append({
                'name': name,
                'url': product_url,
                'image_url': image_url,
                'features': features,
                'sale_price': sale_price,
                'was_price': was_price,
                'stock_info': stock_icons,
                'page_number': page_number
            })
        
        return products
        
    except Exception as e:
        print(f"Error scraping page {page_number}: {str(e)}")
        return []

def save_to_json(products, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'url', 'image_url', 'features', 'sale_price', 'was_price', 'stock_info', 'page_number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            product['features'] = ', '.join(product['features'])
            product['stock_info'] = str(product['stock_info'])
            writer.writerow(product)

def scrape_all_pages():
    all_products = []
    current_page = 1
    json_file = 'centrecom_laptops.json'
    csv_file = 'centrecom_laptops.csv'

    while True:
        print(f"Scraping page {current_page}...")
        products = scrape_laptop_page(current_page)
        
        if not products:
            print(f"No products found on page {current_page}. Stopping.")
            break
        
        all_products.extend(products)
        print(f"Found {len(products)} products on page {current_page}")
        
        # Save after each page
        save_to_json(all_products, json_file)
        save_to_csv(all_products, csv_file)
        print(f"Saved {len(all_products)} total products to files.\n")
        
        current_page += 1
        time.sleep(2)  # Be polite

    return all_products

if __name__ == "__main__":
    laptop_products = scrape_all_pages()
    print(f"Scraping complete. Total products scraped: {len(laptop_products)}")
