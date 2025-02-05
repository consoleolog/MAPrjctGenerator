import inspect
from typing import Any, TypeVar, Type
from langchain_openai import ChatOpenAI

from service.data_service import DataService
from utils.common_utils import set_env
from utils.llm_utils import LLMUtils

T = TypeVar("T")

class IocContainer:
    def __init__(self):
        self.obj_map = {}

    def register(self, obj: Any):
        self.obj_map[type(obj)] = obj

    def get(self, type_: Type[T]) -> T:
        impl_type = type_
        if inspect.isabstract(type_):
            impl_type = type_.__subclasses__()
            if len(impl_type) == 0:
                raise ValueError()
            impl_type = impl_type[0]
        try:
            obj = self.obj_map[impl_type]
        except KeyError:
            raise ValueError()
        return obj

    def compose(self):
        set_env("OPENAI_API_KEY")
        model = ChatOpenAI(model="gpt-4o-mini")
        self.register(model)
        self.register(LLMUtils(self.get(type(model))))
        self.register(DataService(self.get(LLMUtils)))