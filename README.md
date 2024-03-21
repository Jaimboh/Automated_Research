# Automated_Research

Automated_Research is an advanced online application that revolutionizes the research process by automating the collection and analysis of data from the web and public APIs. It facilitates users in conducting comprehensive research on a wide range of topics by simply inputting queries. The application streamlines extracting, processing, and presenting data, making research more efficient and user-friendly.

## Overview

This application leverages Streamlit for its web interface, providing a seamless user experience. It integrates Python libraries such as BeautifulSoup for web scraping and lxml for XML generation, handling data extraction and structuring with precision. Automated_Research is containerized using Docker, ensuring easy deployment and scalability. The project structure includes a main application script (`main.py`), along with modules for source determination, web scraping, data conversion to XML, and integration with OpenAI for enhanced data processing.

## Features

- **User Input for Queries**: Accepts research queries through a text input field.
- **Automated Source Determination**: Automatically identifies the most relevant sources for information retrieval based on the query context.
- **Web Scraping and API Integration**: Gathers data from web pages and public APIs, with the option for users to specify additional sources.
- **Summary and Detailed Views**: Presents the research findings in both summary and detailed formats for comprehensive understanding.
- **Downloadable Results**: Allows for the research results to be downloaded in XML format, facilitating further analysis or reporting.

## Getting started

### Requirements

- Python 3.8 or later
- Streamlit
- BeautifulSoup4
- Requests
- Pandas
- Lxml
- NLTK
- OpenAI

### Quickstart

1. Clone the repository to your local machine.
2. Ensure Docker is installed and running on your system.
3. Build and run the Docker container using `docker-compose up --build`.
4. Access the Streamlit application by navigating to `http://localhost:8501` in your web browser.

### License

Copyright (c) 2024.