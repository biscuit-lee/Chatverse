from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    Base class for all tools.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError("This method should be overridden by subclasses.")