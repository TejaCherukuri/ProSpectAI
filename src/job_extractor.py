from src.chat_model import ChatModel
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from src.utils import clean_text

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
            loader = WebBaseLoader(url)
            page_data = loader.load().pop().page_content
            if not page_data:
                raise ValueError("The scraped page content is empty.")
            cleaned_data = clean_text(page_data)
            print(f"Scraped and cleaned data: {cleaned_data[:200]}...")  # Displaying a snippet of data for debugging
            return cleaned_data
        except Exception as e:
            raise ValueError(f"Error scraping or cleaning the content from the URL {url}: {e}")

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

            # Try parsing the response content into JSON format
            job_data = self.json_parser.parse(res.content)
            print("=====================JSON Job Data==================")
            print(job_data)
            return job_data
        
        except OutputParserException as e:
            raise OutputParserException("Unable to parse job data as valid JSON. The response might be malformed or incomplete.") from e
        except Exception as e:
            raise ValueError(f"An error occurred during job extraction: {e}") from e

