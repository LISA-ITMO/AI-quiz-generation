import box
import yaml
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import HuggingFaceEmbeddings

from haystack.nodes import EmbeddingRetriever, PreProcessor
from haystack.document_stores import WeaviateDocumentStore
from haystack.preview.components.file_converters.pypdf import PyPDFToDocument
import timeit

# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

def run_ingest():
    # Setup for handling UTF-8 encoding specifically or autodetecting
    text_loader_kwargs = {'encoding': 'utf-8'}
    # If you wish to auto-detect encoding, you could instead use:
    # text_loader_kwargs = {'autodetect_encoding': True}

    # Adjust DirectoryLoader to handle .txt files with TextLoader and UTF-8 encoding
    loader = DirectoryLoader(
        cfg.DATA_PATH,
        glob='*.txt',
        loader_cls=TextLoader,
        loader_kwargs=text_loader_kwargs,
        recursive=True,  # Assuming you want to search directories recursively
        show_progress=True,
        use_multithreading=True,
        max_concurrency=4
    )

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE,
                                                   chunk_overlap=cfg.CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=cfg.EMBEDDINGS,
                                       model_kwargs={'device': 'cpu'})

    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(cfg.DB_FAISS_PATH)

if __name__ == "__main__":
    run_ingest()
