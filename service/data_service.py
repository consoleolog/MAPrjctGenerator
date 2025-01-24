import ast
import json
import os

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from unstructured_pytesseract import pytesseract

from logger import LoggerFactory
from prompts.extract_key_value_prompt import extract_key_value_prompt
from utils import data_utils
from utils.llm_utils import LLMUtils, extract_xml
import easyocr

class DataService:
    def __init__(self, llm_utils: LLMUtils):
        self.llm_utils = llm_utils
        self.logger = LoggerFactory().get_logger(__class__.__name__, "MindApply")

    def extract_key_value(self, file_path):
        pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'
        ocr_reader = easyocr.Reader(["ko", "ko"])
        results = ocr_reader.readtext(file_path)

        docs = "\n".join(str(result[1]) for result in results)

        data_processing_steps = extract_key_value_prompt(docs)

        input_txt = f"{docs}"

        self.logger.debug(f"Input Text:\n{input_txt}")

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
        for key in keys:
            data_utils.save_data(key,1, os.getcwd()+"/train.csv")
        for value in values:
            data_utils.save_data(value,0, os.getcwd()+"/train.csv")

    def get_model(self):
        train_csv = pd.read_csv("train.csv")
        train_csv.drop_duplicates(subset=["text"], inplace=True)
        text = train_csv["text"]
        unique_txt = text.tolist()
        unique_txt = ''.join(unique_txt)
        unique_txt = list(set(unique_txt))
        unique_txt.sort()

        tokenizer = Tokenizer(char_level=True, oov_token="<OOV>")

        txt_list = train_csv["text"].tolist()
        tokenizer.fit_on_texts(txt_list)

        world_index = tokenizer.word_index
        self.logger.debug(f"\nWorld Index: {world_index}")

        train_seq = tokenizer.texts_to_sequences(txt_list)

        y_data = train_csv["label"].tolist()
        train_csv["length"] = text.str.len()

        max_len = train_csv["length"].max()

        X = pad_sequences(train_seq, maxlen=max_len)

        trainX, valX, trainY, valY = train_test_split(X, y_data, test_size=0.2, random_state=42)

        model = tf.keras.models.Sequential([
            tf.keras.layers.Embedding(len(world_index) + 1, 16),
            tf.keras.layers.LSTM(128),
            tf.keras.layers.Dense(1, activation="sigmoid")
        ])
        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
        model.fit(np.array(trainX), np.array(trainY), epochs=100, validation_data=(np.array(valX), np.array(valY)))
