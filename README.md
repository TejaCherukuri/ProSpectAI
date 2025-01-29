# ProSpectAI: The Smart Way to Reach Out to Recruiters

Get tailored job application messages at the click of a button. ProSpectAI helps you craft personalized emails to recruiters based on the job posting and your resume. It leverages the power of LLMs (Language Models) and all new Deepseek-R1 to generate thoughtful, context-aware responses.

The app also includes a unique "DeepThink" feature of DeepSeek-R1, that provides insight into the reasoning process behind the generated message, giving users transparency and confidence in the model's output.

### Prompt Engineering
The prompts used for generating messages and extracting job details have been carefully engineered and refined through multiple iterations to ensure accuracy and relevance. These prompts, referred to as `message_prompt` and `extract_prompt` in the code, are central to the functionality of ProSpectAI. Feel free to explore and adjust them after cloning the repo to suit your specific needs.



## Deployed Version

ProSpectAI is deployed and running on [Hugging Face Spaces](https://huggingface.co/spaces/tejacherukuri/ProSpectAI). Try it out for yourself!

## Features

- **LLM-Powered Message Generation**: ProSpectAI uses latest Deepseek-R1 model to generate contextually relevant and concise messages to recruiters, tailored to job descriptions and your resume.
- **DeepThink Insights**: In addition to the generated message, ProSpectAI provides insights into the thought process behind the model's decision-making, helping you understand how it tailored the message.
- **Natural Language Processing**: Seamlessly integrates your resume and job descriptions to craft messages that stand out.

## Technologies & Tools Used

- **LangChain**: For building and chaining language models and pipelines.
- **Python**: For building the backend logic and integration with the API.
- **Groq API Integration**: To power the language model and make API calls to Groq’s Deepseek-R1 model.
- **Streamlit**: For building an interactive web interface.

## Limitations

While ProSpectAI offers powerful functionality, there are some constraints due to the current limits set by **Groq Cloud**:

- **Tokens**: 6000 tokens per minute.
- **Requests**: 30 requests per minute.

These limitations can affect the responsiveness of the application under heavy usage. However, the system can scale with proper adjustments in API usage and token allocation.

## Scope

This tool is designed to streamline the process of reaching out to recruiters by providing a custom email generator, but it can be further extended to:
- **Multi-language support**.
- **Integration with LinkedIn and other professional networks** for automatic job description extraction.
- **Advanced analytics**: Provide deeper insights into recruiter engagement and response patterns.

We are continuously improving the system and will incorporate feedback from the community.

## Getting Started

To run the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tejacherukuri/ProSpectAI.git
   cd ProSpectAI

2. **Set up the environment**:
   - Create a virtual environment (optional but recommended):
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows, use venv\Scripts\activate
     ```
   
   - Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set up the Groq API key**:
   - Add your **GROQ_API_KEY** to your environment variables. You can set it in your terminal like this:
     ```bash
     export GROQ_API_KEY="your-api-key"  # On Windows, use set instead of export
     ```

4. **Run the Streamlit app**:
   - Once the environment is set up, you can run the application with Streamlit:
     ```bash
     streamlit run app.py
     ```

5. **Access the app**:
   - After running the above command, you should be able to access the app in your web browser at the following URL:
     ```
     http://localhost:8501
     ```

## Raise an Issue or Start a Discussion

If you encounter any bugs, limitations, or have any suggestions for improvements, please feel free to [raise an issue](https://github.com/tejacherukuri/ProSpectAI/issues) or start a discussion. We welcome contributions and feedback!

## Contributing

Feel free to fork the repository, make improvements, and create a pull request. Your contributions are much appreciated!
