import os

import google.generativeai as genai
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from loguru import logger

from scraper import run_complete
from utils import load_json, dict_to_text

load_dotenv()
os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_text_chunks(text, chunk_size=50000, chunk_overlap=10000):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_embeddings(model):
    embeddings = GoogleGenerativeAIEmbeddings(model=model)
    return embeddings


def save_vector_store(text_chunks, project_name, model="models/embedding-001"):
    embeddings = get_embeddings(model=model)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(f"./assets/{project_name}/faiss_index")


def get_conversational_chain(model="gemini-pro", temperature=0.1):
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model=model, temperature=temperature)

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question, project_name, embedding_model = "models/embedding-001", llm = "gemini-pro", temperature = 0.1):
    embeddings = get_embeddings(model=embedding_model)

    new_db = FAISS.load_local(
        f"./assets/{project_name}/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True,
    )
    docs = new_db.similarity_search(user_question)
    # logger.info(docs[0].page_content)
    chain = get_conversational_chain(model = llm, temperature = temperature)

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True
    )

    logger.success(response)
    return response




def run_pipeline(
    homepage_url,
    user_question,
    project_name,
    scrape_fresh=True,
    read_fresh=True,
    scrape_depth=None,
    save_db=True,
    embedding_model = "models/embedding-001",
    llm = "gemini-pro",
    temperature = 0.1,
):
    extracted_data_dict = run_complete(
        homepage_url,
        project_name=project_name,
        scrape_fresh=scrape_fresh,
        read_fresh=read_fresh,
        scrape_depth=scrape_depth,
    )

    raw_text = dict_to_text(extracted_data_dict)
    text_chunks = get_text_chunks(raw_text)
    logger.debug(text_chunks)

    if save_db:
        save_vector_store(text_chunks= text_chunks, project_name= project_name, model= embedding_model)
        logger.success(f"Vector store saved for {project_name}")
    else:
        if os.path.exists(f"./assets/{project_name}/faiss_index/index.pkl") and os.path.exists(f"./assets/{project_name}/faiss_index/index.faiss"):
            logger.info(f"Vector store already saved for {project_name}. Okay to move forward")
        else:
            logger.error(f"No vector DB found for {project_name}. Please enable the creation of the Database atleast once!")
        
    response = user_input(user_question = user_question, project_name = project_name, embedding_model = embedding_model, llm = llm, temperature= temperature)
    return response

if __name__ == "__main__":
    homepage_url = "https://ravi0531rp.github.io/web-rag/index.html"
    user_question = (
        "What is the accuracy for Object Detection Classifier and which model is used?"
    )
    project_name = "WEB_RAG_DEMO"
    response = run_pipeline(homepage_url, 
        user_question, 
        project_name, 
        scrape_fresh = False,
        read_fresh = True,
        scrape_depth = None,
        save_db = False,
        embedding_model = "models/embedding-001",
        llm = "gemini-pro",
        temperature = 0.1)
