import streamlit as st
from chat_gemini_faiss import run_pipeline
from utils import add_punctuation

def run(homepage_url, user_question, project_name, scrape_fresh, read_fresh, scrape_depth, save_db, embedding_model, llm, temperature):
    return f"Running with parameters: homepage_url={homepage_url}, user_question={user_question}, project_name={project_name}, scrape_fresh={scrape_fresh}, read_fresh={read_fresh}, scrape_depth={scrape_depth}, save_db={save_db}, embedding_model={embedding_model}, llm={llm}, temperature={temperature}"


def main():
    st.title("Web RAG")
    st.markdown("---")

    col1, col2 = st.columns(2)
    
    # Left column for scraping-related fields
    with col1:
        st.markdown("### Scraping Settings")
        with st.expander("Scraping Options"):
            # Dropdown for scrape_fresh
            scrape_fresh_options = [True, False]
            scrape_fresh = st.selectbox("Scrape fresh data?", scrape_fresh_options, format_func=lambda x: 'Yes' if x else 'No')

            # Dropdown for read_fresh
            read_fresh_options = [True, False]
            read_fresh = st.selectbox("Read fresh data?", read_fresh_options, format_func=lambda x: 'Yes' if x else 'No')

            # Input field for scrape depth
            scrape_depth = st.text_input("Enter scrape depth", key="scrape_depth_input", value= "NA")

    # Right column for LLM and VectorDB fields
    with col2:
        st.markdown("### LLM and VectorDB Settings")
        with st.expander("Model Options"):
            # Dropdown for embedding model
            embedding_models = ["models/embedding-001", "models/embedding-002", "models/embedding-003", "astradb"]
            embedding_model = st.selectbox("Select embedding model", embedding_models)

            # Dropdown for llm
            llms = ["gemini-pro", "llama2", "phi2", "open-AI"]
            llm = st.selectbox("Select language model", llms)

            # Input field for temperature
            temperature = st.text_input("Enter temperature", value="0.1", key="temperature_input")

            # Dropdown for save_db
            save_db_options = [True, False]
            save_db = st.selectbox("Save to database?", save_db_options, format_func=lambda x: 'Yes' if x else 'No')

    # Input field for Project Name
    project_name = st.text_input("Enter your Project Name", key="project_name")

    # Input field for URL
    homepage_url = st.text_input("Enter homepage URL", key="url_input")

    # Input field for user query
    user_question = st.text_input("Enter your question", key="query_input")

    # Button to run the final function
    if st.button("Run"):
        try:
            response = run_pipeline(homepage_url, 
            user_question, 
            project_name, 
            scrape_fresh = scrape_fresh,
            read_fresh = read_fresh,
            scrape_depth = scrape_depth,
            save_db = save_db,
            embedding_model = embedding_model,
            llm = llm,
            temperature = temperature)["output_text"]

            with st.spinner("Executing..."):
                st.success("Function executed successfully!")
                st.markdown("---")
                st.info("Result:")
                st.write(add_punctuation(response))
    
        except Exception as e:
            st.error(f"Error: {e}")
            st.markdown("---")
            st.info("Result:")
            st.write(f"Failure: Please Check the Parameters")


# Add custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if __name__ == "__main__":
    local_css("./style/styles.css")
    main()
