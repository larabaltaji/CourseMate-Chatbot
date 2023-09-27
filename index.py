import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = "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"

def create_index() -> None: 

    # Get loaders for each pdf file (lectures + syllabus)

    loaders = [
        PyPDFLoader("Lectures/MSBA316-SU2023-Syllabus.pdf"),
        PyPDFLoader("Lectures/Lecture_01_introduction_Summer22_23.pdf"),
        PyPDFLoader("Lectures/Lecture_02_TextPreprocessing_Summer22_23.pdf"),
        PyPDFLoader("Lectures/Lecture_03_feature_engineering_Summer22_23.pdf"),
        PyPDFLoader("Lectures/Lecture_04_language_models_Summer22_23.pdf"),
        PyPDFLoader("Lectures/Lecture_05_Sequence_Labeling_Summer22_23.pdf"),
        PyPDFLoader("Lectures/Lecture_06_Text_Classification_SA_Summer22_23.pdf"),
        PyPDFLoader("Lectures/Lecture_07_Text_Similarity_Clustering_Summer22_23.pdf"),
        PyPDFLoader("Lectures/Lecture_08_Topic_Modeling_Summarization_Summer22_23.pdf")
    ]

    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    # Splitting the documents into smaller chunks

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 150
    )
    splits = text_splitter.split_documents(docs)

    # Creating embeddings for each chunk and saving them to a vector store 

    embedding = OpenAIEmbeddings()
    persist_directory = 'db'
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectordb.persist()

create_index()