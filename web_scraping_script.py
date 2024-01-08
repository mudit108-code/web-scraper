import requests
from bs4 import BeautifulSoup
import csv
import json

def get_page_content(url):
    try:
        # Send an HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        return response.text

    except requests.RequestException as e:
        print(f"Error during request: {e}")
        return None

def extract_data_from_page(html_content):
    if html_content:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract quotes, authors, and tags using BeautifulSoup methods
        quotes = [quote.text.strip() for quote in soup.find_all('span', class_='text')]
        authors = [author.text.strip() for author in soup.find_all('small', class_='author')]
        tags = [tag.text.strip() for tag in soup.find_all('div', class_='tags')]

        return quotes, authors, tags

    return None, None, None

def save_to_csv(quotes, authors, tags):
    data_list = []

    # Combine the extracted data into a list of dictionaries
    for quote, author, tag in zip(quotes, authors, tags):
        data = {
            'Quote': quote,
            'Author': author,
            'Tags': tag,
        }
        data_list.append(data)

    # Save the data to both CSV and JSON files
    with open('quotes_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Quote', 'Author', 'Tags']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)

    with open('quotes_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=2)

def main():
    base_url = "http://quotes.toscrape.com"
    quotes_url = "/page/1/"

    full_url = base_url + quotes_url

    # Fetch HTML content of the page
    html_content = get_page_content(full_url)

    # Extract data from the page
    quotes, authors, tags = extract_data_from_page(html_content)

    if quotes and authors and tags:
        # Save the extracted data to CSV and JSON
        save_to_csv(quotes, authors, tags)
        print("Data extraction and saving completed successfully.")
    else:
        print("Data extraction failed.")

if __name__ == "__main__":
    main()
