from src.chat_model import ChatModel
from langchain_core.prompts import PromptTemplate
import re
import requests

class MessageWriter:
    """
    A class that generates personalized email messages for recruiters based on job descriptions and resumes.
    The class utilizes a prompt-based approach to generate the email content in a natural, casual tone, 
    while focusing on the alignment between the job requirements and the applicant's skills and experiences.

    Attributes:
    -----------
    chat_model : ChatModel
        An instance of the ChatModel used to process the job description and resume, and generate the email content.
    message_prompt : PromptTemplate
        The template used to instruct the model on how to structure the email content based on the job and resume details.

    Methods:
    --------
    write_message(job: str, resume: str) -> tuple:
        Generates the email message content by processing the job description and resume through the prompt chain,
        and returns both the extracted thought process and cleaned email content.
    """

    def __init__(self):
        """
        Initializes the MessageWriter instance with the necessary models and prompt template for email generation.
        """
        self.chat_model = ChatModel()

        # Define the prompt template for generating recruiter emails
        self.message_prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### YOUR RESUME
            {resume}

            ### INSTRUCTION:
            You are a very helpful AI agent.
            Your job is to write an email to the recruiter regarding the job mentioned above describing the capability of your work, 
            skills and experience (seen in resume above) in fulfilling their needs.

            Follow the instructions line by line
            At each line, stop, read and reason.
            Finally, consolidate all together to a final email.
            
            Your instructions start now
            1. You should sound very natural
            2. Use the information only from your resume provided above. DO NOT HALLUCINATE
            3. Think from the recuiter perspective and what he loves to see.
            4. Identify the top responsibilities, skills and qualifications from the job description.
            5. Identify the skills, relevant work experience and research experience points from resume that matches the extracted details of job.
            6. Once identified, write how does these skills and experience fulfill the responsibilities for the new role. Do not be generic, rather write what specific experiences can prove your claim. Use quantification when necessary, from your work experience points.
            7. Highlight how you will fit in to their team with the qualifications you possess. Make it sound natural.
            8. AVOID, "I am so excited to apply", "my skills align well".
            9. AVOID, "Thank you for considering my application, I look forward to discussing how my skills align with the organizational goals". Instead, write the same information in a creative way.
            10. DO NOT make it too professional, do it in a casual tone.
            11. Make it CONCISE and the limit to 8-10 lines. Divide into paragraphs.
            12. Embed portfolio and other necessary links within the email where necessary. Add full link, not a placeholder.
            13. Signature should be "Best\n, Name of the person from the resume". No links, here.
            14. AVOID PREAMBLE. For Example: AVOID, "Here's an email, etc" at the start of generation.

            ### EMAIL:
            """
        )

    def write_message(self, job, resume):
        """
        Generates a personalized email message for the recruiter based on the provided job description and resume.

        Parameters:
        -----------
        job : str
            The job description from the job listing.
        resume : str
            The resume content of the applicant.

        Returns:
        --------
        tuple:
            A tuple containing:
            - thought_process (str): The reasoning and thought process of the model.
            - cleaned_response (str): The final generated email content, cleaned of any extra elements.

        Raises:
        -------
        ValueError: If there is an error in invoking the model chain or processing the response.
        """
        try:
            # Create the chain of prompt and model invocation
            message_chain = self.message_prompt | self.chat_model.groq

            # Invoke the model to generate the email content
            res = message_chain.invoke(input={"job_description": job, "resume": resume})

            # Extract the thought process (if any) enclosed in <think> tags
            think_content = re.findall(r'<think>(.*?)</think>', res.content, flags=re.DOTALL)
            cleaned_response = re.sub(r'<think>.*?</think>', '', res.content, flags=re.DOTALL)

            # Check if content was found
            if think_content:
                # Get the first element from the list (since re.findall returns a list)
                extracted_text = think_content[0]
                extracted_text = extracted_text.strip()  # Strip leading/trailing whitespace and newlines

                # Print the well-formatted text
                print(f"=== Thought Process ===\n {extracted_text}")
                think_content = extracted_text
            else:
                print("No content found between <think> and </think> tags.")

            print(f"=== Cleaned Response ===\n {cleaned_response}")

            # Return the extracted thought process and the cleaned email content
            return think_content, cleaned_response.strip()
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 413:
                raise ValueError("The input is too large. Please reduce the size and try again.")
            elif http_err.response.status_code == 429:
                raise ValueError("Too many requests. Please try again later.")
            else:
                raise ValueError(f"HTTP error occurred: {http_err}") from http_err
        except Exception as e:
            # Raise a ValueError with additional context if there was an error in processing
            raise ValueError(f"An error occurred while generating the email: {e}") from e
