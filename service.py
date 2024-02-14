import streamlit as st
import PyPDF2
import io
from llm import initialize_llm_service
from llama_index import VectorStoreIndex
import asyncio

st.title("💬 Quiz Quest")

uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

class Document:
    def __init__(self, content):
        self.content = content
        # Generate a unique ID for the document, could be a hash of the content or any unique identifier
        self.doc_id = hash(content)
    
    def get_doc_id(self):
        return self.doc_id
    
    # Assuming there's a 'hash' attribute or method needed as per the error message
    @property
    def hash(self):
        return hash(self.content)

# Use this Document class to wrap your extracted text
def extract_text_from_pdf(file):
    with io.BytesIO(file.getvalue()) as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text() if page.extract_text() else ''
        return text

async def generate_quiz(uploaded_file):
    extracted_text = extract_text_from_pdf(uploaded_file)
    if extracted_text:
        llm, service_context = await initialize_llm_service()
        document = Document(extracted_text)  # Wrap the extracted text in a Document object
        documents = [document]  # Now 'documents' is a list of Document objects
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        query_engine = index.as_query_engine()

        prompt = 'Сформулируй тест: вопрос по теме урока из загруженного файла и возможный ответ к нему.'
        response = query_engine.query(prompt).response
        return response
    else:
        raise ValueError("Unable to extract text from the uploaded file.")

if uploaded_file is not None:
    quiz_result = asyncio.run(generate_quiz(uploaded_file))
    st.write(quiz_result)
