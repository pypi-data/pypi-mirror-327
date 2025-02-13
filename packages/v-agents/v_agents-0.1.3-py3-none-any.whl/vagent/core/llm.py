import os
import json
import inspect
import aiohttp
import asyncio
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional, Callable, List, Tuple


@dataclass
class Conversation:
    role: str
    content: str


def parse_function_signature(func: Callable):
    signature = inspect.signature(func)
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    for name, param in signature.parameters.items():
        prop_info = {
            "type": "string",
            "description": f"The '{name}' parameter",
        }
        # Example special case for 'unit'
        if name == "unit":
            prop_info["enum"] = ["celsius", "fahrenheit"]

        parameters["properties"][name] = prop_info
        if param.default is param.empty:
            parameters["required"].append(name)
    data = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "This function has no description.",
            "parameters": parameters,
        },
    }
    return data


class LLMEngine:
    def __init__(
        self,
        default_model: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.default_model = default_model
        if base_url is None:
            base_url = os.environ.get("RC_API_BASE", None)
        if api_key is None:
            api_key = os.environ.get("RC_API_KEY", None)
        assert base_url is not None, "base_url is required"
        assert api_key is not None, "api_key is required"
        self.base_url = base_url
        self.api_key = api_key

    def prepare_input(
        self,
        tools: Optional[List[Callable]],
        response_format: Optional[BaseModel] = None,
    ):
        if response_format and hasattr(response_format, "model_json_schema"):
            return_type = {
                "type": "json_schema",
                "json_schema": {
                    "name": "foo",
                    "schema": response_format.model_json_schema(),
                },
            }
            return None, return_type
        elif tools:
            return [parse_function_signature(tool) for tool in tools], None
        else:
            return None, None

    def prepare_payload(
        self,
        messages: List[Conversation],
        temperature: Optional[float] = 0.3,
        model: Optional[str] = None,
        tools: Optional[List[Callable]] = None,
        response_format: Optional[BaseModel] = None,
    ) -> Tuple[bool, dict]:
        tools, return_format = self.prepare_input(tools, response_format)
        endpoint = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "response_format": return_format,
            "stream": False if tools else True,
            "tools": tools,
        }
        return endpoint, headers, payload

    async def _async_call_chat(
        self,
        messages: List[Conversation],
        temperature: Optional[float] = 0.3,
        model: Optional[str] = None,
        tools: Optional[List[Callable]] = None,
        response_format: Optional[BaseModel] = None,
    ):
        endpoint, headers, payload = self.prepare_payload(
            messages, temperature, model, tools, response_format
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"Request failed [{resp.status}]: {text}")
                result = await resp.json()
                result = result["choices"][0]["message"]["content"]
                return result

    async def _async_call_chat_stream(
        self,
        messages: List[Conversation],
        temperature: Optional[float] = 0.3,
        model: Optional[str] = None,
        tools: Optional[List[Callable]] = None,
        response_format: Optional[BaseModel] = None,
    ):
        if tools:
            raise NotImplementedError("Tools are not supported in stream mode.")
        endpoint, headers, payload = self.prepare_payload(
            messages, temperature, model, tools, response_format
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"Request failed [{resp.status}]: {text}")
                async for chunk in resp.content:
                    chunk = chunk.decode().replace("data: ", "").strip()
                    if not chunk:
                        continue
                    chunk = json.loads(chunk)["choices"]
                    if len(chunk) == 0:
                        continue
                    chunk = chunk[0]["delta"]["content"]
                    if chunk:
                        yield chunk

    def __call__(
        self,
        messages: List[Conversation],
        temperature: Optional[float] = 0.3,
        model: Optional[str] = None,
        tools: Optional[List[Callable]] = None,
        response_format: Optional[BaseModel] = None,
    ):
        loop = asyncio.get_event_loop()
        if tools:
            # non stream mode
            result = loop.run_until_complete(
                self._async_call_chat(
                    messages=messages,
                    temperature=temperature,
                    model=model,
                    tools=tools,
                    response_format=response_format,
                )
            )
        else:
            results = []

            async def runner():
                async for chunk in self._async_call_chat_stream(
                    messages=messages,
                    temperature=temperature,
                    model=model,
                    tools=tools,
                    response_format=response_format,
                ):
                    results.append(chunk)

            loop.run_until_complete(runner())
            result = "".join(results)

        result = self.post_process(result, tools, response_format)
        return result

    def post_process(
        self,
        result: str,
        tools: Optional[List[Callable]],
        response_format: Optional[BaseModel],
    ):

        if response_format and hasattr(response_format, "model_validate"):
            validated_result = response_format.model_validate(json.loads(result))
            return validated_result
        elif tools:
            result = json.loads(result)
            return result
        return result


if __name__ == "__main__":
    messages = [{"role": "user", "content": "What's the weather like in New York?"}]
    llm = LLMEngine("meta-llama/Llama-3.3-70B-Instruct")

    async def main():
        async for chunk in llm.call_chat(messages):
            print(chunk, end="", flush=True)

    asyncio.run(main())
