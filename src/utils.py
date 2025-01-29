import re

def clean_text(text: str) -> str:
    """
    Cleans and preprocesses the input text by removing unwanted elements such as HTML tags, URLs,
    special characters, and extra whitespace. This function is useful for preparing text data for
    further processing or analysis.

    Parameters:
    -----------
    text : str
        The input text to be cleaned. This text may contain HTML tags, URLs, special characters,
        multiple spaces, and unnecessary whitespace.

    Returns:
    --------
    str
        A cleaned version of the input text with the following modifications:
        - HTML tags removed
        - URLs removed
        - Special characters (other than letters, digits, and spaces) removed
        - Multiple consecutive spaces replaced with a single space
        - Leading and trailing whitespace removed
        - Extra spaces between words reduced to a single space

    Example:
    --------
    >>> clean_text("<p>Hello <b>World</b>! Visit http://example.com for more info.</p>")
    'Hello World Visit for more info'
    """
    
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove special characters (anything that is not a letter, number, or space)
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    
    # Trim leading and trailing whitespace
    text = text.strip()
    
    # Remove extra whitespace between words (in case of multiple spaces)
    text = ' '.join(text.split())
    
    return text
