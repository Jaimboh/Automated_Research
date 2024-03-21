import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Download necessary NLTK datasets
    nltk.download('punkt')
    nltk.download('stopwords')
except Exception as e:
    logging.error("Error downloading NLTK datasets", exc_info=True)

def determine_sources(query):
    """
    Analyzes the query to determine potential sources for information retrieval.
    """
    try:
        # Preprocessing the query
        query = query.lower()
        query_tokens = word_tokenize(query)
        filtered_tokens = [word for word in query_tokens if word not in stopwords.words('english')]
        
        # Hardcoded rules for identifying sources based on query context
        potential_sources = {
            'corporate_misconduct': ['https://eyfinancialservicesthoughtgallery.ie/wp-content/uploads/2016/08/EY_Global_Fraud_Survey.pdf', 'https://publicapis.dev/api'], 
            'technical_specifications': ['https://senzahydrogen.com/understanding-pem-electrolyzer-components.html', 'https://publicapis.dev/api'],
        }
        
        # Determining the potential sources based on filtered tokens
        sources = []
        if 'misconduct' in filtered_tokens or 'corporate' in filtered_tokens:
            sources.extend(potential_sources['corporate_misconduct'])
        if 'specifications' in filtered_tokens or 'technical' in filtered_tokens:
            sources.extend(potential_sources['technical_specifications'])
        
        logging.info("Sources determined successfully for query: " + query)
        # Return a list of URLs (web and API) as potential sources
        return sources
    except Exception as e:
        logging.error("Error determining sources for query", exc_info=True)
        return []

def include_user_sources(sources, additional_urls, additional_apis):
    """
    Appends user-specified URLs and APIs to the list of determined sources.

    Parameters:
    - sources (list): The list of automatically determined sources.
    - additional_urls (list): User-specified URLs for web scraping.
    - additional_apis (list): User-specified APIs for data retrieval.

    Returns:
    - Updated list of sources including user-specified URLs and APIs.
    """
    try:
        if additional_urls:
            sources.extend(additional_urls)
        if additional_apis:
            sources.extend(additional_apis)
        logging.info("User-specified sources included successfully.")
        return sources
    except Exception as e:
        logging.error("Error including user-specified sources", exc_info=True)
        return sources

# Example usage (for testing, can be commented out or removed)
if __name__ == '__main__':
    example_query = "misconducts in EY and how they have been addressed"
    try:
        sources = determine_sources(example_query)
        logging.info("Identified sources for example query:")
        for source in sources:
            logging.info(source)

        additional_urls = ["https://example.com"]
        additional_apis = ["https://api.example.com"]
        try:
            sources = include_user_sources(sources, additional_urls, additional_apis)
            logging.info("Final list of sources including user inputs:")
            for source in sources:
                logging.info(source)
        except Exception as e:
            logging.error("Error in example usage of include_user_sources", exc_info=True)
            
    except Exception as e:
        logging.error("Error in example usage of determine_sources", exc_info=True)