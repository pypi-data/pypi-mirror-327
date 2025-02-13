import os
from loguru import logger
from langfuse import Langfuse
from langfuse.client import StatefulTraceClient


class AgentLogger:
    def __init__(self, enable_logger: bool = True, enable_langfuse: bool = False):
        langfuse_public_key = os.environ.get("LANGFUSE_PUBLIC_KEY", None)
        langfuse_secret_key = os.environ.get("LANGFUSE_SECRET_KEY", None)
        self.enable_logger = enable_logger
        self.enable_langfuse = enable_langfuse
        if langfuse_public_key and langfuse_secret_key and enable_langfuse:
            self.langfuse = Langfuse()
        else:
            self.langfuse = None

    def func_call(self, info):
        if self.enable_logger:
            logger.info(f"[Function Call] {info}")

    def get_trace(self, name: str) -> StatefulTraceClient:
        trace = self.langfuse.trace(name=name)
        return trace
