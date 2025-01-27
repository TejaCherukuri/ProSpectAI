from chat_model import ChatModel
from langchain_core.prompts import PromptTemplate
import re

class MessageWriter:
    def __init__(self, ):
        self.chat_model = ChatModel()
        self.message_prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### YOUR RESUME
            {resume}

            ### INSTRUCTION:
            You are Teja and you are applying for a job.
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
            13. Signature should be "Best\n, Teja Krishna Cherukuri"
            14. AVOID PREAMBLE. For Example: AVOID, "Here's an email, etc" at the start of generation.
            
            Remember that you are Teja.

            ### EMAIL:
            """
        )

    def write_message(self, job, resume):
        message_chain = self.message_prompt | self.chat_model.groq
        res = message_chain.invoke(input={"job_description": job, "resume": resume})

        think_content = re.findall(r'<think>(.*?)</think>', res.content, flags=re.DOTALL)
        cleaned_response = re.sub(r'<think>.*?</think>', '', res.content, flags=re.DOTALL)

        # Check if content was found
        if think_content:
            # Get the first element from the list (since re.findall returns a list)
            extracted_text = think_content[0]

            # Strip leading/trailing whitespace and newlines
            extracted_text = extracted_text.strip()

            # Print the well-formatted text
            think_content = extracted_text
            print("======Thought Process======")
            print(think_content)
        else:
            print("No content found between <think> and </think> tags.")
        
        print("======Cleaned Response======")
        print(cleaned_response)

        return think_content, cleaned_response.strip()