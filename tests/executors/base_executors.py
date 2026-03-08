from abc import ABC, abstractmethod


class BaseExecutors(ABC):
    @abstractmethod
    def execute(self):
        pass
