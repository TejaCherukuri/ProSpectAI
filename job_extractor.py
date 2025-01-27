from chat_model import ChatModel
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

class JobExtractor:
    def __init__(self, ):
        self.chat_model = ChatModel()
        self.extract_prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills`, `responsibilities`, `basic qualifications`,
            `preferred qualifications` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        self.json_parser = JsonOutputParser()

    def parse_job_from_web(self, url):
        loader = WebBaseLoader(url)
        docs = loader.load()

        for i in range(len(docs)):
            print(docs[i].page_content)
            print(docs[i].metadata)

        return docs.pop()

    def extract_jobdata(self, text):
        extract_chain = self.extract_prompt | self.chat_model.groq
        res = extract_chain.invoke(input={"page_data": text})
        try:
            res = self.json_parser.parse(res.content)
            print("=====================JSON Job Data==================")
            print(res)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res