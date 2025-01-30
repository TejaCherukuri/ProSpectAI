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

    # Add GitHub repository link
    st.markdown("[🔗 View on GitHub](https://github.com/tejacherukuri/ProSpectAI)")

    # Resume Upload Section
    st.subheader("Upload Your Resume")
    uploaded_file = st.file_uploader("Upload a PDF Resume", type=["pdf"])

    # Job Input Option (Radio Buttons for Job URL or Description)
    input_option = st.radio(
        "How would you like to provide the job information?",
        ("Job URL", "Job Description")
    )

    job_url = None
    job_description = None

    # Show corresponding input field based on the selection
    if input_option == "Job URL":
        job_url = st.text_input(
            "Enter the Job URL",
            placeholder="https://amazon.jobs/en/jobs/2831138/software-development-engineer-2025-ai-ml"
        )
        
        # Display the alert with color
        with st.expander("🔔 **Alert!** Job URL Instructions", expanded=True):
            st.markdown(
                """
                <p style="color:red;">If using a LinkedIn job URL (Easy Apply), paste the job description instead.</p>
                """, unsafe_allow_html=True)

    elif input_option == "Job Description":
        job_description = st.text_area("Enter the Job Description", height=200)


    # Button to trigger the flow
    if st.button("Generate Message"):
        if job_url or job_description:
            try:
                st.info("Processing your request...")
                # Trigger the flow (replace with your logic)
                thought, response = generate_message_for_job(job_url, uploaded_file, job_description)

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
            except ValueError as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.error("Please provide a valid job URL.")

def generate_message_for_job(job_url, uploaded_file, job_description=None):
    
    # Load the resume using the appropriate method (PDF or text)
    if uploaded_file:
        resume_loader = ResumeLoaderFactory.create_loader("pdf")
        resume = resume_loader.load_resume(uploaded_file)
    else:
        resume_loader = ResumeLoaderFactory.create_loader("text")
        resume = resume_loader.load_resume()

    # Extract the key info from job URL
    extractor = JobExtractor()
    if job_url:
        job_description = extractor.parse_job_from_web(job_url)

    job = extractor.extract_jobdata(job_description)
    if not job or not job.get('job_postings'):
        raise ValueError(f"Cannot fetch job details from this url: {job_url}, Use the 'Job Description' field for better assistance!")

    # Invoke chat model
    writer = MessageWriter()
    thought, message = writer.write_message(job, resume)

    return thought, message

if __name__ == "__main__":
    main()
