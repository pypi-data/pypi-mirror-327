from ._base import CodeExecutor
from typing import List, Callable, Dict


class LocalFuncExecutor(CodeExecutor):
    def __init__(self, tools: List[Callable]):
        super().__init__()
        self.tools = tools

    def __call__(self, llm_output: Dict, **kwargs):
        if "type" not in llm_output or llm_output["type"] != "function":
            raise ValueError(f"Expected function output, but got {llm_output}")
        if llm_output["name"] not in [tool.__name__ for tool in self.tools]:
            raise ValueError(f"Function {llm_output['name']} not in tools")

        func_body = self.tools[
            [tool.__name__ for tool in self.tools].index(llm_output["name"])
        ]

        if not callable(func_body):
            raise ValueError(f"Function {llm_output['name']} not callable")

        try:
            parameters = llm_output["parameters"].keys()
            func_kwargs = {}
            for param in parameters:
                if param in kwargs:
                    func_kwargs[param] = kwargs[param]
                    locals()[param] = kwargs[param]
                else:
                    func_kwargs[param] = llm_output["parameters"][param]

            func_execution = func_body(**func_kwargs)
        except Exception as e:
            raise ValueError(f"Error parsing function parameters: {e}")

        return func_execution
