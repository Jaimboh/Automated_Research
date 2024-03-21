import streamlit as st
from lxml import etree
from source_determination import determine_sources, include_user_sources
import base64
from web_scraping import scrape_data, fetch_api_data
from openai_integration import OpenAIIntegration
import logging
import os

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the title of the application
st.title('Automated Research Application')

# Initialize OpenAI Integration
openai_integration = OpenAIIntegration()

# Function to parse XML data
def parse_xml_data(xml_string):
    """
    Parses XML data and returns a dictionary representation.
    """
    result = {}
    try:
        root = etree.fromstring(xml_string)
        for child in root:
            category = child.tag
            items = []
            for item in child:
                item_data = {}
                for data_point in item:
                    item_data[data_point.tag] = data_point.text
                items.append(item_data)
            result[category] = items
    except Exception as e:
        logging.error("Failed to parse XML data", exc_info=True)
        st.error("Failed to parse XML data.")
        st.error(f"Error details: {e}")
    return result

# Function to generate a download link for the XML data
def generate_download_link(xml_content, filename="ResearchResults.xml", text="Download XML file"):
    """
    Generates a download link for an XML file.
    
    Parameters:
    - xml_content (str): XML content to be downloaded.
    - filename (str): Name for the downloaded file.
    - text (str): Text to display on the download button.
    
    Returns:
    - A Streamlit download button element with the download link.
    """
    b64 = base64.b64encode(xml_content.encode()).decode()
    href = f'<a href="data:file/xml;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Creating a sidebar for user inputs
st.sidebar.header('User Input Options')

try:
    # Text input for research query
    query = st.sidebar.text_input('Enter your research query here:', '')

    # Check box for OpenAI model integration
    use_openai = st.sidebar.checkbox('Use OpenAI for research', False)

    # Text area for specifying additional sources via URL
    additional_urls = st.sidebar.text_area("Specify additional source URLs (one per line):", "").split("\n")
    additional_urls = [url.strip() for url in additional_urls if url.strip()]

    # Text area for specifying additional sources via API selection
    additional_apis = st.sidebar.text_area("Specify additional APIs (one per line):", "").split("\n")
    additional_apis = [api.strip() for api in additional_apis if api.strip()]

    # Placeholder for summary view
    st.header('Summary View')
    summary_placeholder = st.empty()
    summary_placeholder.text('Summary results will be displayed here.')

    # Placeholder for detailed view
    st.header('Detailed View')
    details_placeholder = st.empty()
    details_placeholder.text('Detailed results will be displayed here.')

    if query:
        sources_determined = False
        if use_openai:
            try:
                openai_response = openai_integration.fetch_response_from_openai(query)
                # Properly structure the OpenAI response to fit into the application's XML data structure
                root = etree.Element("ResearchResults")
                response_element = etree.SubElement(root, "response")
                content_element = etree.SubElement(response_element, "content")
                content_element.text = openai_response
                xml_data = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()

                # Display OpenAI response directly without parsing into dictionary
                st.header('OpenAI Response (Summary)')
                st.write(openai_response)
                st.header('OpenAI Response (Detailed)')
                st.write(openai_response)

                # Generate and display the download button for the OpenAI response in XML format
                download_button = generate_download_link(xml_data)
                st.markdown(download_button, unsafe_allow_html=True)
                sources_determined = True
            except Exception as e:
                logging.error("Failed to fetch response from OpenAI", exc_info=True)
                st.error("An error occurred while fetching response from OpenAI.")
                st.error(f"Error details: {e}")
        else:
            try:
                sources = determine_sources(query)
                sources = include_user_sources(sources, additional_urls, additional_apis)
                sources_determined = True
                # Display the potential sources (for demonstration purposes)
                st.write("Identified sources for your query:")
                for source in sources:
                    st.write(source)
            except Exception as e:
                logging.error("An error occurred while determining sources", exc_info=True)
                st.error("An error occurred while determining sources.")
                st.error(f"Error details: {e}")

        if sources_determined and not use_openai:
            # Placeholder for actual data fetching and processing logic
            # Here we simulate the process of fetching and parsing XML data received from the backend.
            # This is a placeholder XML data. Replace it with actual XML data from the backend.
            xml_data = """<?xml version='1.0' encoding='UTF-8'?>
<ResearchResults>
    <misconducts>
        <Item>
            <title>Issue 1</title>
            <description>Description of issue 1</description>
        </Item>
        <Item>
            <title>Issue 2</title>
            <description>Description of issue 2</description>
        </Item>
    </misconducts>
    <technical_specifications>
        <Item>
            <component>Component 1</component>
            <specs>Specs of component 1</specs>
        </Item>
        <Item>
            <component>Component 2</component>
            <specs>Specs of component 2</specs>
        </Item>
    </technical_specifications>
</ResearchResults>"""
            parsed_data = parse_xml_data(xml_data)

            # Displaying the summary and detailed views
            for category, items in parsed_data.items():
                with st.expander(f"{category.capitalize()} (Summary)"):
                    for item in items:
                        st.write(f"Title: {item.get('title', item.get('component', 'N/A'))}")
                with st.expander(f"{category.capitalize()} (Detailed)"):
                    for item in items:
                        st.write(item)

            # Generate and display the download button for the XML data
            download_button = generate_download_link(xml_data)
            st.markdown(download_button, unsafe_allow_html=True)

    st.success("Streamlit application initialized successfully.")
except Exception as e:
    logging.error("An error occurred while initializing the Streamlit application", exc_info=True)
    st.error("An error occurred while initializing the Streamlit application.")
    st.error(f"Error details: {e}")