from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    Base class for all tools.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    """
    Define the schema for the tool's arguments.
    """
    @abstractmethod
    def argument_schema(self) -> dict:
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def execute(self, arguments):
        raise NotImplementedError("This method should be overridden by subclasses.")