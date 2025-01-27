import os
from langchain_community.document_loaders import TextLoader

class ResumeLoader:
    def __init__(self, ):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.current_dir, "resources", "resume.txt")

    def load_resume(self): 
        # Load the text file
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} does not exist. Please check the path.")
        
        text_loader = TextLoader(self.file_path)
        resume = text_loader.load()  # Directly load the full text without chunking

        print(resume[0].page_content)

        return resume[0]
