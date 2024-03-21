from lxml import etree
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_xml_document(data):
    """
    Converts the extracted data into an XML document.

    Parameters:
    - data (dict): The extracted information from web scraping and API calls.

    Returns:
    - An XML string representation of the data.
    """
    try:
        # Create the root element
        root = etree.Element("ResearchResults")

        # Iterate over the data dictionary and create corresponding XML elements
        for category, items in data.items():
            category_element = etree.SubElement(root, category)
            if isinstance(items, list):
                for item in items:
                    item_element = etree.SubElement(category_element, "Item")
                    if isinstance(item, dict):
                        for key, value in item.items():
                            key_element = etree.SubElement(item_element, key)
                            key_element.text = str(value)
                    else:
                        item_element.text = str(item)
            else:
                category_element.text = str(items)

        # Convert the XML tree to a string
        xml_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        logging.info("XML document created successfully.")
        return xml_string
    except Exception as e:
        logging.error("Failed to create XML document.", exc_info=True)
        raise e

# Example usage
if __name__ == "__main__":
    try:
        sample_data = {
            'misconducts': [
                {'title': 'Issue 1', 'description': 'Description of issue 1'},
                {'title': 'Issue 2', 'description': 'Description of issue 2'},
            ],
            'technical_specifications': [
                {'component': 'Component 1', 'specs': 'Specs of component 1'},
                {'component': 'Component 2', 'specs': 'Specs of component 2'},
            ]
        }
        xml_result = create_xml_document(sample_data)
        print(xml_result)
    except Exception as e:
        logging.error("Error in example usage of create_xml_document.", exc_info=True)