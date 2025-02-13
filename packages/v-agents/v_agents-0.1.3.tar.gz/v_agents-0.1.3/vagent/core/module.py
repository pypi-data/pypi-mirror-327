from .context import VContext


class VModule:
    def __init__(self):
        self.ctx = VContext()

    def forward(self, *args, **kwargs):
        ...

    def __call__(self, *args, **kwargs):
        self.forward(*args, **kwargs)