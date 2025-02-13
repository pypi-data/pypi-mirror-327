from typing import Optional, List, Callable, Any
from pydantic import BaseModel

from .registry import FUNC_REGISTRY
from .llm import LLMEngine, Conversation, parse_function_signature
from .context import VContext


def execute_llm_program(
    ctx: VContext,
    llm: LLMEngine,
    system_prompt: str,
    messages: List[Conversation],
    response_format: BaseModel,
    temperature: float,
    tools: Optional[List[Callable]],
    kwargs: dict,
):
    messages = [{"role": "system", "content": system_prompt}] + messages
    return llm(
        messages=messages,
        temperature=temperature,
        tools=tools,
        response_format=response_format,
    )


def llm_program(
    model: str,
    temperature: float = 0.6,
    max_tokens: int = 1024,
    tools: Optional[List[Callable]] = None,
) -> Callable:
    """
    Decorator for creating llm programs.
    Args:
        model (str): The model to use.
        temperature (float): The temperature to use.
        max_tokens (int): The maximum number of tokens to use.
        tools (List[Callable]): The tools to use.
    """

    def decorator(function):
        def parameterized_llm_call(*args, **kwargs):
            assert args, "You must provide at least one argument (context)."
            assert isinstance(
                args[0], VContext
            ), "The first argument must be an VContext."
            ctx = args[0]
            system_message = function.__doc__ or ""
            response_format = function.__annotations__.get("return", None)
            llm = LLMEngine(default_model=model)
            message = function(*args, **kwargs)
            messages = []
            messages.append({"role": "user", "content": message})
            return execute_llm_program(
                ctx=ctx,
                llm=llm,
                system_prompt=system_message,
                messages=messages,
                response_format=response_format,
                temperature=temperature,
                tools=tools,
                kwargs=kwargs,
            )

        return parameterized_llm_call

    return decorator


def tool(func: Callable):
    FUNC_REGISTRY[func.__name__] = parse_function_signature(func)

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
