import os

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI

from fi.integrations.otel import LangChainInstrumentor, register
from fi.integrations.otel.types import ProjectType

# Configure trace provider with custom evaluation tags
trace_provider = register(
    project_type=ProjectType.OBSERVE,
    project_name="LANGCHAIN_TEST_OBSERVE",
    project_version_name="V8",
    # eval_tags=eval_tags,
)

# Initialize the LangChain instrumentor
LangChainInstrumentor().instrument(tracer_provider=trace_provider)


def create_rag_pipeline(pdf_folder):
    # Load all PDF documents from the folder
    documents = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())

    if not documents:
        raise ValueError(f"No PDF files found in {pdf_folder}")

    # Split text into chunks - using RecursiveCharacterTextSplitter for better handling of PDF content
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    texts = text_splitter.split_documents(documents)

    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    vectorstore = FAISS.from_documents(texts, embeddings)

    # Create retrieval chain
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
        ),
    )

    return qa_chain


def run_qa_chain(qa_chain, queries):
    """Run queries through the QA chain."""
    results = []
    for query in queries:
        try:
            result = qa_chain.invoke({"query": query})
            # print(f"\nQA Chain - Question: {query}")
            # print(f"Answer: {result['result']}")
            results.append(result)
        except Exception as e:
            print(f"Error processing QA query '{query}': {str(e)}")
    return results


def main():
    # Ensure OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Please set OPENAI_API_KEY environment variable")

    try:
        # Initialize RAG pipeline
        pdf_folder = "documents"
        if not os.path.exists(pdf_folder):
            raise ValueError(f"PDF folder '{pdf_folder}' does not exist")

        # Create RAG chain
        qa_chain = create_rag_pipeline(pdf_folder)

        # Example queries for RAG
        qa_queries = [
            "What is the main topic of the documents?",
            "Can you summarize the key points across all documents?",
            "What is rstarmath?",
        ]

        # Run RAG chain
        print("\n=== Running QA Chain ===")
        run_qa_chain(qa_chain, qa_queries)

    except Exception as e:
        print(f"Error in main execution: {str(e)}")


if __name__ == "__main__":
    main()
