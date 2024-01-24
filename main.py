import os
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the values
gradient_access_token = os.getenv('GRADIENT_ACCESS_TOKEN')
gradient_workspace_id = os.getenv('GRADIENT_WORKSPACE_ID')





