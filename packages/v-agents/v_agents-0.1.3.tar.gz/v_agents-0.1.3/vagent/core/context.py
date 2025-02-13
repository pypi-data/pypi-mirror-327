from typing import Any


class VContext:
    def __init__(self):
        self.context = {}

    def put(self, key: str, value: Any):
        self.context[key] = value

    def get(self, key: str, default: Any) -> Any:
        return self.context.get(key, default)
