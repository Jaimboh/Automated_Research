import requests
from bs4 import BeautifulSoup
import logging
import json

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_html_content(url):
    """
    Fetches the HTML content of a given URL.

    Parameters:
    - url (str): The URL to fetch the HTML content from.

    Returns:
    - BeautifulSoup object if the request is successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching HTML content from {url}: {e}", exc_info=True)
        return None

def scrape_data(url):
    """
    Scrapes relevant data from the given URL.

    This is a placeholder function and should be customized based on the HTML
    structure of the target websites.

    Parameters:
    - url (str): The URL to scrape data from.

    Returns:
    - dict: A dictionary containing the scraped data.
    """
    soup = fetch_html_content(url)
    if soup:
        # Example of scraping a specific element. This should be replaced with real scraping logic.
        # For example, to scrape titles: title = soup.find('h1').get_text()
        # This placeholder should be replaced with actual scraping logic based on the target web page.
        # return {'title': title}
        # Placeholder return value to demonstrate the concept. Replace with actual scraping logic.
        return {'data': 'Scraped data goes here'}
    else:
        logging.error(f"Failed to fetch or parse HTML content from {url}")
        return {'error': 'Failed to fetch or parse HTML content.'}

def fetch_api_data(api_url, api_key=None):
    """
    Fetches data from a public API.

    Parameters:
    - api_url (str): The URL of the public API.
    - api_key (str, optional): An API key for APIs that require authentication.

    Returns:
    - A dictionary containing the API response data or an error message.
    """
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        logging.info("Successfully fetched data from API", extra={'api_url': api_url})
        return response.json()  # Parse and return the JSON data
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 429:
            logging.error("API rate limit exceeded. Please try again later.")
        else:
            logging.error("HTTP error occurred", exc_info=True)
    except requests.exceptions.RequestException as req_err:
        logging.error("Error fetching data from API", exc_info=True)
    except ValueError as json_err:
        logging.error("Error parsing JSON response", exc_info=True)

    # Return an error message in case of failures
    return {'error': 'Failed to fetch or parse API data.'}