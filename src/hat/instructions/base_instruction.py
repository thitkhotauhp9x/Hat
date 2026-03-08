from abc import ABC, abstractmethod


class BaseInstruction(ABC):
    @abstractmethod
    def get_instruction(self) -> str:
        pass
