from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from config.constants import *
load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")
def get_model_client():
    openai_model_client = OpenAIChatCompletionClient(
        model=MODEL,
        api_key=api_key)

    return openai_model_client