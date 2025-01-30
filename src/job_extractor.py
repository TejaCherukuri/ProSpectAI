from src.chat_model import ChatModel
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from src.utils import clean_text
import json
import requests


class JobExtractor:
    """
    A class responsible for extracting job posting details from a given job listing URL. The class uses 
    a prompt-based approach to process scraped text and extract relevant job details.

    Attributes:
    -----------
    chat_model : ChatModel
        An instance of the ChatModel to handle processing and extraction.
    extract_prompt : PromptTemplate
        The template used to instruct the model on how to process the scraped text.
    json_parser : JsonOutputParser
        The output parser to convert model responses into structured JSON format.

    Methods:
    --------
    parse_job_from_web(url: str) -> str:
        Scrapes and cleans the content from a given job listing URL.
    
    extract_jobdata(text: str) -> dict:
        Extracts and parses the job data from the cleaned text into a structured JSON format.
    """

    def __init__(self):
        """
        Initializes the JobExtractor instance with the necessary models, prompt templates, 
        and output parsers.
        """
        self.chat_model = ChatModel()

        # Define the template to extract job data using the language model
        self.extract_prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: 
            `role`, `experience`, `skills`, `responsibilities`, `basic qualifications`, 
            `preferred qualifications`, and `description`.
            Only return the valid JSON.
            If you do not find any data to form a JSON, return 
            ```json{{'job_postings': []}}```
            ### VALID JSON (NO PREAMBLE):
            """
        )

        self.json_parser = JsonOutputParser()

    def parse_job_from_web(self, url):
        """
        Scrapes and cleans the content from a given job listing URL.

        Parameters:
        -----------
        url : str
            The URL of the job listing page.

        Returns:
        --------
        str:
            The cleaned text content extracted from the job listing page.
        
        Raises:
        -------
        ValueError: If the content could not be loaded or cleaned properly.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            loader = WebBaseLoader(url, headers)
            page_data = loader.load().pop().page_content

            # Check for blocking or unsupported browser messages
            if "unsupported browser" in page_data.lower():
                raise ValueError(f"Unsupported browser message detected.")
                # return None

            if not page_data:
                raise ValueError(f"Failed to fetch content from the URL {url}.")
        
            print(f"===Page Data===\n {page_data}")

            cleaned_data = clean_text(page_data)
            print(f"=== Scraped and cleaned data ===\n {cleaned_data}...")  # Displaying a snippet of data for debugging
            return cleaned_data
        except Exception as e:
            print(f"WebBaseLoader Error: {e}")
            # raise ValueError(f"Failed to fetch content from the URL {url}.")
            return None
        

    def extract_jobdata(self, text):
        """
        Extracts and parses the job data from the cleaned text into a structured JSON format.

        Parameters:
        -----------
        text : str
            The cleaned text content from the job listing page.

        Returns:
        --------
        dict:
            A dictionary containing the extracted job information in JSON format.

        Raises:
        -------
        OutputParserException: If the extracted response cannot be parsed as valid JSON.
        ValueError: If the extraction process fails.
        """
        try:
            extract_chain = self.extract_prompt | self.chat_model.groq
            res = extract_chain.invoke(input={"page_data": text})

            print(f"=== Result Content ===\n {res.content}")

            if not res.content.strip():  # Check if response is empty
                raise ValueError("No valid job data extracted.")

            try:
                job_data = self.json_parser.parse(res.content)
                print(f"=== JSON Job Data ===\n {job_data}")
                return job_data
            except json.decoder.JSONDecodeError:
                print("Invalid JSON received. Returning empty job data.")
                return {"job_postings": []}  # Fail gracefully
            
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 413:
                raise ValueError("The input is too large. Please reduce the size and try again.")
            elif http_err.response.status_code == 429:
                raise ValueError("Too many requests. Please try again later.")
            else:
                raise ValueError(f"HTTP error occurred: {http_err}") from http_err
        except OutputParserException as e:
            raise OutputParserException("Unable to parse job data as valid JSON.") from e
        except Exception as e:
            raise ValueError(f"An error occurred during job extraction: {e}") from e


