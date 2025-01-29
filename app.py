import streamlit as st
from src.resume_loader import ResumeLoaderFactory
from src.job_extractor import JobExtractor
from src.message_writer import MessageWriter

def main():
    # Set the page layout to wide mode
    st.set_page_config(page_title="ProSpectAI: The Smart Way to Reach Out to Recruiters", layout="wide")

    # Title of the app
    st.title("ProSpectAI: The Smart Way to Reach Out to Recruiters")
    st.markdown("Tailored job application messages at the click of a button.")

    # Resume Upload Section
    st.subheader("Upload Your Resume")
    uploaded_file = st.file_uploader("Upload a PDF Resume", type=["pdf"])

    # Input field for the job URL
    job_url = st.text_input(
        "Enter the Job URL",
        placeholder="https://amazon.jobs/en/jobs/2831138/software-development-engineer-2025-ai-ml"
    )

    # Button to trigger the flow
    if st.button("Generate Message"):
        if job_url:
            st.info("Processing your request...")
            # Trigger the flow (replace with your logic)
            thought, response = generate_message_for_job(job_url, uploaded_file)

            # Create two columns for displaying outputs side by side
            col1, col2 = st.columns(2)

            # Display Thought Process in the first column
            with col1:
                st.subheader("DeepThink")
                st.text_area(" ", value=thought, height=500)

            # Display Generated Message in the second column
            with col2:
                st.subheader("Generated Message")
                st.text_area(" ", value=response, height=500)
        else:
            st.error("Please provide a valid job URL.")

def generate_message_for_job(job_url, uploaded_file):
    
    # Load the resume using the appropriate method (PDF or text)
    if uploaded_file:
        resume_loader = ResumeLoaderFactory.create_loader("pdf")
        resume = resume_loader.load_resume(uploaded_file)
    else:
        resume_loader = ResumeLoaderFactory.create_loader("text")
        resume = resume_loader.load_resume()

    # Extract the key info from job URL
    extractor = JobExtractor()
    job = extractor.parse_job_from_web(job_url)
    job = extractor.extract_jobdata(job)

    # Invoke chat model
    writer = MessageWriter()
    thought, message = writer.write_message(job, resume)

    return thought, message

if __name__ == "__main__":
    main()
