from abc import ABC, abstractmethod


class BaseReviewer(ABC):
    @abstractmethod
    def review(self):
        pass
