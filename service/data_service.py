import ast
import json
import os

from unstructured_pytesseract import pytesseract
from logger import LoggerFactory
from prompts.extract_key_value_prompt import extract_key_value_prompt
from utils import data_utils
from utils.common_utils import set_env
from utils.llm_utils import LLMUtils, extract_xml
import easyocr

class DataService:
    def __init__(self, llm_utils: LLMUtils):
        self.llm_utils = llm_utils
        self.logger = LoggerFactory().get_logger(__class__.__name__, "MindApply")

    def extract_key_value(self, file_path):
        os.environ['KMP_DUPLICATE_LIB_OK']='True'
        pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'
        ocr_reader = easyocr.Reader(["ko", "ko"], gpu=True)
        results = ocr_reader.readtext(file_path)

        docs = "\n".join(str(result[1]) for result in results)

        data_processing_steps = extract_key_value_prompt(docs)

        input_txt = f"{docs}"

        # self.logger.debug(f"Input Text:\n{input_txt}")

        format_response = self.llm_utils.chain(input_txt, data_processing_steps)

        response = extract_xml(format_response, "response")

        self.logger.debug(f"Format Response:\n{response}")

        if type(response) == list:
            data = response
        else:
            try:
                data = json.loads(response)
            except json.JSONDecodeError as e:
                self.logger.warning(f"JSON parsing err - {str(e)}")
                data = ast.literal_eval(response)
        keys = data_utils.extract_keys_from_list(data)
        values = data_utils.extract_values_from_list(data)
        self.logger.debug(f"Keys:\n{keys}")
        self.logger.debug(f"Values:\n{values}")
        for key in keys:
            data_utils.save_data(key,1, os.getcwd()+"/train.csv")
        for value in values:
            data_utils.save_data(value,0, os.getcwd()+"/train.csv")
