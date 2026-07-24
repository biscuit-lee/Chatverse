from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def generate(self, messages: list[dict], tools: list[dict]):
        raise NotImplementedError("This method should be overridden by subclasses.")

    
