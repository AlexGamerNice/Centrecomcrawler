import re
import requests
from bs4 import BeautifulSoup

def extract_product_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    
    # Find all product containers
    product_grid = soup.find('div', class_='product-grid')
    if not product_grid:
        return products
        
    for product in product_grid.find_all('div', class_='prbox_box'):
        product_data = {
            'name': None,
            'sales_points': [],
            'badges': [],
            'sale_price': None,
            'was_price': None,
            'stock_status': [],
            'image_url': None,
            'product_url': None
        }
        
        # Extract product name
        name_div = product.find('div', class_='prbox_name')
        if name_div:
            product_data['name'] = name_div.get_text(strip=True)
        
        # Extract sales points
        sales_points_div = product.find('div', class_='prbox_salespoints')
        if sales_points_div:
            sales_points_ul = sales_points_div.find('ul')
            if sales_points_ul:
                product_data['sales_points'] = [
                    li.get_text(strip=True) for li in sales_points_ul.find_all('li')
                ]
        
        # Extract badges
        badges_div = product.find('div', class_='prbox_badges')
        if badges_div:
            badges_ul = badges_div.find('ul')
            if badges_ul:
                product_data['badges'] = [
                    li.get_text(strip=True) for li in badges_ul.find_all('li')
                ]
        
        # Extract prices
        pricebox = product.find('div', class_='prbox_pricebox')
        if pricebox:
            sale_price = pricebox.find('div', class_='saleprice')
            if sale_price:
                product_data['sale_price'] = sale_price.get_text(strip=True)
            
            was_price = pricebox.find('div', class_='wasprice')
            if was_price:
                product_data['was_price'] = was_price.get_text(strip=True)
        
        # Extract stock status
        stock_icons = product.find_all('div', class_='prbox_icon')
        for icon in stock_icons:
            tooltip = icon.find('div', class_='tooltip')
            if tooltip:
                icon_element = icon.find('i')
                icon_class = ' '.join(icon_element['class']) if icon_element else None
                status = {
                    'icon_class': icon_class,
                    'status_text': tooltip.get_text(strip=True)
                }
                product_data['stock_status'].append(status)
        
        # Extract image URL from data-lazy attribute
        if product.has_attr('data-lazy'):
            match = re.search(r'url\((.*?)\)', product['data-lazy'])
            if match:
                product_data['image_url'] = match.group(1)
        
        # Extract product URL
        link = product.find('a', class_='prbox_link')
        if link and link.has_attr('href'):
            product_data['product_url'] = link['href']
        
        products.append(product_data)
    
    return products

# Get URL from user input and fetch content
url = input("Enter the URL to scrape: ")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise error for bad status codes
    
    products = extract_product_data(response.text)
    for idx, product in enumerate(products, 1):
        print(f"Product #{idx}:")
        for key, value in product.items():
            print(f"  {key}: {value}")
        print("\n" + "-"*50 + "\n")
        
except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")