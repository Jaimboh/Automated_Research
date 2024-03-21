import openai
import os
import logging

# Setting up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpenAIIntegration:
    def __init__(self):
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if openai.api_key is None:
                raise ValueError("OPENAI_API_KEY environment variable is not set. INPUT_REQUIRED {Set your OpenAI API key in the environment variables.}")
            logging.info("OpenAI API key has been set successfully.")
        except Exception as e:
            logging.error("Failed to initialize OpenAI API key.", exc_info=True)
            raise e

    def fetch_response_from_openai(self, query):
        try:
            # Adjust the model as per requirement. You might want to use "text-davinci-003" or any other available models.
            response = openai.Completion.create(engine="davinci", prompt=query, max_tokens=100)
            logging.info("Successfully fetched response from OpenAI.")
            return response.choices[0].text.strip()
        except openai.error.OpenAIError as oe:
            logging.error("OpenAI API error occurred.", exc_info=True)
            raise oe
        except Exception as e:
            logging.error("An error occurred while fetching response from OpenAI.", exc_info=True)
            raise e

# Example usage
if __name__ == "__main__":
    try:
        openai_integration = OpenAIIntegration()
        query = "Explain the significance of machine learning in today's technology."
        response = openai_integration.fetch_response_from_openai(query)
        print("Response from OpenAI:", response)
    except Exception as e:
        logging.error("Failed to fetch response from OpenAI for the query.", exc_info=True)