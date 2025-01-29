from langchain_groq import ChatGroq
import os

class ChatModel:
    """
    A wrapper class around the `ChatGroq` model, allowing interaction with the Groq AI model for generating responses.

    Attributes:
    -----------
    groq : ChatGroq
        The instance of the `ChatGroq` class used for generating responses from the Groq model.
        The model is initialized with specific configuration parameters like temperature, API key, and model type.
    """
    
    def __init__(self):
        """
        Initializes the ChatModel class and sets up the ChatGroq instance for communication with the Groq model.

        The constructor sets up the model configuration, including:
        - `temperature`: Controls the randomness of the model's responses. Lower values (e.g., 0) make the output more deterministic.
        - `api_key`: The API key required to authenticate requests to the Groq model, fetched from the environment variables.
        - `model`: The specific Groq model to use. In this case, it uses the "deepseek-r1-distill-llama-70b" model.

        The API key is fetched securely from the environment variables, ensuring that sensitive information is not hardcoded.

        Raises:
        -------
        EnvironmentError:
            If the API key is not set in the environment variables, an exception will be raised.
        """
        
        api_key = os.getenv("GROQ_API_KEY")
        
        # Raise an error if the API key is not found in the environment
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY environment variable not set.")
        
        # Initialize the Groq model with the given configuration
        self.groq = ChatGroq(
            temperature=0, 
            api_key=api_key, 
            model="deepseek-r1-distill-llama-70b"
        )
