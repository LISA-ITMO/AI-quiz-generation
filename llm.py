import os
from dotenv import load_dotenv
from llama_index import ServiceContext, set_global_service_context
from llama_index.embeddings import GradientEmbedding
from llama_index.llms import GradientBaseModelLLM
import asyncio

# Load environment variables from .env file
load_dotenv()

async def initialize_llm_service():
    gradient_access_token = os.getenv('GRADIENT_ACCESS_TOKEN')
    gradient_workspace_id = os.getenv('GRADIENT_WORKSPACE_ID')

    # Define the Gradient's Model Adapter for Mixtral
    llm = GradientBaseModelLLM(
        base_model_slug="mixtral-8x7b-instruct",
        max_tokens=510,
    )

    # Configure Gradient embeddings
    embed_model = GradientEmbedding(
        gradient_access_token=gradient_access_token,
        gradient_workspace_id=gradient_workspace_id,
        gradient_model_slug="bge-large",
    )

    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        chunk_size=512,
    )

    set_global_service_context(service_context)
    return llm, service_context