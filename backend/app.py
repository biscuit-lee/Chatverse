import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify

from scrapers import walmartScraper

""" 
def scrape(url):
    # URL of the test website
    url = 'http://example.com'
        
    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find and print the title of the page
    title = soup.find('title').get_text()
    print('Page Title:', title)

    # Find and print all paragraph texts
    paragraphs = soup.find_all('p')
    for i, paragraph in enumerate(paragraphs, start=1):
        print(f'Paragraph {i}:', paragraph.get_text())

 """
app = Flask(__name__)


@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello from the backend!'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)