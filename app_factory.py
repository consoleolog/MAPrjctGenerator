from langchain_ollama import ChatOllama

from service.data_service import DataService
from utils.llm_utils import LLMUtils

class AppFactory:
    def __init__(self):
        self.model = ChatOllama(model="exaone3.5")
        self.llm_utils = LLMUtils(self.model)
        self.data_service = DataService(self.llm_utils)