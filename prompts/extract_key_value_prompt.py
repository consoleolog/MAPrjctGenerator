def extract_key_value_prompt(context: str):
    return [
        """
        문서의 항목들을 출력해줘.
        단 문서에 있는것만 출력해
        절대 글자를 임의로 만들거나 수정하지마.
        """,
        f"""
                    자료 : {context}
                    자료 중에 문서에 없는 Key 가 있으면 삭제 하고 남은 것은 JSON 형태로 출력해줘
                    Example:
                    ```json
                    {{
                        "key": "value"
                    }}
                    ```
                    """,
        """
        JSON 데이터를 분석해서 파이썬 딕셔너리(Dict) 형태로 출력해
        Example Format:
        ```python
        {
            "key": "value"
        }
        ```
        """,
        """
        Python 데이터를 분석해서 각각의 딕셔너리(Dict)들을 List 에 담아줘
        Example Format:
        ```python
        [{ "key": "value" }, {"key2": "value2"}]
        ``` 
        """,
        """
        Python 데이터를 분석해서 아무것도 건드리지말고 리스트 그대로 다음과 같은 Format 에 담아줘 
        절대 코드를 작성하지마 그냥 반환만해 제발
        Example Format:
        <response>
        [{ "key": "value" }, {"key2": "value2"}]
        <response>
        """
    ]