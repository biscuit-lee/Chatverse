from playwright.sync_api import sync_playwright

def scrape_walmart_product(product_name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        #walmart_url = f'https://www.walmart.com/{product_name}'
        #page.goto(walmart_url)
        
        page.goto('https://www.target.com/')
        # Search for the product
        page.fill('input[aria-label="What can we help you find? suggestions appear below"]', product_name)
        page.press('input[aria-label="What can we help you find? suggestions appear below"]', 'Enter')
    
        # Wait for the results to load

        page.wait_for_selector('span[data-test="current-price"]')

        # Extract product details
        page.screenshot(path='screenshot.png')

        price_elements = page.query_selector_all('span[data-test="unit-price"]')
        product_containers = page.query_selector_all('div[data-test="product-details"]')
        results = []


        for container in product_containers:
            try:
                # Locate the product title
                product_title_element = container.query_selector('a[data-test="product-title"] div')
                product_title = product_title_element.get_attribute('title').strip()
                
                # Locate the price
                price_element = container.query_selector('span[data-test="unit-price"]')
                price = price_element.inner_text().strip()
                
                # Store the product details and price together
                results.append({'product_title': product_title, 'price': price})
                
                print(f"Product Title: {product_title}, Price: {price}")
            except Exception as e:
                print(f"Error extracting product details: {e}")
                
        browser.close()
    return results

if __name__ == "__main__":
    product_name = "chicken"
    results = scrape_walmart_product(product_name)
    """for result in results:
        print(result)
    """