import os
import tempfile
from abc import ABC, abstractmethod
from langchain_community.document_loaders import TextLoader, PyPDFLoader

class ResumeLoader(ABC):
    """
    Abstract Base Class for loading resumes. All resume loader classes (TextResumeLoader, PdfResumeLoader)
    should inherit from this class and implement the `load_resume` method.

    Methods:
    --------
    load_resume() -> object:
        Abstract method to load a resume. Must be implemented by subclasses.
    """
    
    @abstractmethod
    def load_resume(self):
        """
        Abstract method to load a resume. Must be implemented by subclasses.

        Returns:
        --------
        object:
            The content of the resume as an object.
        """
        pass

class TextResumeLoader(ResumeLoader):
    """
    A class to load resumes from a text file.

    Methods:
    --------
    load_resume() -> object:
        Loads the resume from a predefined text file located in the "resources" directory.
        Raises a FileNotFoundError if the file is not found.
    
    Raises:
    -------
    FileNotFoundError: If the predefined resume text file is not found.
    """
    
    def __init__(self):
        """
        Initializes the TextResumeLoader instance and sets the path to the resume text file.
        """
        self.current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(self.current_dir, "resources", "resume.txt")

    def load_resume(self): 
        """
        Loads the resume from a predefined text file.

        Returns:
        --------
        object:
            The resume content as an object containing the text.

        Raises:
        -------
        FileNotFoundError:
            If the resume text file cannot be found at the specified path.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} does not exist. Please check the path.")
        
        text_loader = TextLoader(self.file_path)
        resume = text_loader.load()  # Directly load the full text without chunking
        print(f"=== Resume Content ===\n {resume[0].page_content}")

        return resume[0]

class PdfResumeLoader(ResumeLoader):
    """
    A class to load resumes from PDF files.

    Methods:
    --------
    load_resume_pdf(file) -> object:
        Loads a resume from an uploaded PDF file, saving it temporarily before processing.
        Cleans up the temporary file after processing.

    Raises:
    -------
    Exception:
        If an error occurs during the loading or extraction of the PDF content.
    """
    
    def load_resume(self, file=None):
        """
        Loads the resume from an uploaded PDF file by saving it as a temporary file and processing it.

        Parameters:
        -----------
        file : file-like object
            The uploaded PDF file to be processed.

        Returns:
        --------
        object:
            The resume content as an object extracted from the PDF file.

        Raises:
        -------
        Exception:
            If an error occurs during the loading or extraction of the PDF content.
        """
        if file is None:
            raise ValueError("PDF file must be provided for PdfResumeLoader.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.getvalue())  # Save uploaded file
            temp_file_path = temp_file.name  # Get file path

        try:
            # Load PDF using the temporary file path
            pdf_loader = PyPDFLoader(temp_file_path)
            resume = pdf_loader.load()  # Extract text from PDF
            
            print(f"=== Resume Content ===\n {resume[0].page_content}")
            return resume[0]

        except Exception as e:
            raise Exception(f"Error loading PDF: {e}")

        finally:
            # Ensure the file is deleted after processing
            os.remove(temp_file_path)

class ResumeLoaderFactory:
    """
    A Factory class responsible for creating appropriate ResumeLoader instances based on the input type (text or PDF).

    Methods:
    --------
    create_loader(file_type: str) -> ResumeLoader:
        Returns an instance of ResumeLoader based on the specified file type (text or pdf).
    """
    
    @staticmethod
    def create_loader(file_type: str) -> ResumeLoader:
        """
        Creates a ResumeLoader instance based on the file type provided.

        Parameters:
        -----------
        file_type : str
            The type of file to be processed ("text" or "pdf").

        Returns:
        --------
        ResumeLoader:
            The appropriate ResumeLoader instance for the specified file type.

        Raises:
        -------
        ValueError:
            If the file type is not recognized (must be either "text" or "pdf").
        """
        if file_type == "text":
            return TextResumeLoader()
        elif file_type == "pdf":
            return PdfResumeLoader()
        else:
            raise ValueError("Invalid file type. Accepted values are 'text' or 'pdf'.")
