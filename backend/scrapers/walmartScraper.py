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
        page.screenshot(path='screenshot.png')

        page.wait_for_selector('div[data-automation-id="product-price"]')

        # Extract product details
        products = page.query_selector_all('div[data-automation-id="product-price"]')
        results = []

        for product in products:
            dollar = product.locator('span.f2').inner_text()
            cents = product.locator('span.f6').nth(1).inner_text()
            results.append(f"${dollar}.{cents}")
            print(f"Dollar: {dollar}, Cents: {cents}")

        browser.close()
        return results

if __name__ == "__main__":
    product_name = "chicken"
    results = scrape_walmart_product(product_name)
    for result in results:
        print(result)
