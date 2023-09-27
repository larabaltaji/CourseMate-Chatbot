import os
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = "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"

def create_conversation() -> ConversationalRetrievalChain:

    persist_directory = 'db'
    embeddings = OpenAIEmbeddings()

    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )

    document_content_description = "Lecture notes"

    metadata_field_info = [
        AttributeInfo(
            name="source",
            description="""If the question is about general information of the course or the instructor and not related to a specific lecture, the chunk should be from
            "Lectures/MSBA316-SU2023-Syllabus.pdf",
            Otherwise, if the question is related to a specific lecture or a specific topic in the course, the lecture the chunk is from, should be one of
            "Lectures/Lecture_01_introduction_Summer22_23.pdf",
            "Lectures/Lecture_02_TextPreprocessing_Summer22_23.pdf",
            "Lectures/Lecture_03_feature_engineering_Summer22_23.pdf",
            "Lectures/Lecture_04_language_models_Summer22_23.pdf",
            "Lectures/Lecture_05_Sequence_Labeling_Summer22_23.pdf",
            "Lectures/Lecture_06_Text_Classification_SA_Summer22_23.pdf",
            "Lectures/Lecture_07_Text_Similarity_Clustering_Summer22_23.pdf",
            or "Lectures/Lecture_08_Topic_Modeling_Summarization_Summer22_23.pdf" 
            """,
            type="string",
        ),
        AttributeInfo(
            name="page",
            description="The page from the lecture.",
            type="integer",
        ),
    ]

    llm = OpenAI(temperature=0)
    retriever = SelfQueryRetriever.from_llm(
        llm,
        db,
        document_content_description,
        metadata_field_info,
        verbose=True
    )
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, then just say that you don't know, and appologize for any inconvinience.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)

    qa = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        chain_type='stuff',
        retriever= retriever,
        memory=memory,
        get_chat_history=lambda h: h,
        verbose=True,
        combine_docs_chain_kwargs={'prompt': QA_CHAIN_PROMPT}
    )


    return qa