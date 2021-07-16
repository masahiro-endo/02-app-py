from abc import ABCMeta, abstractmethod
from gamemode import GAMEMODE

# 大元になる抽象基底クラス


class AbstractScene(metaclass=ABCMeta):
    def __init__(self):
        self.GAMEMODE = GAMEMODE

    @abstractmethod
    def update(self) -> bool:
        pass

    @abstractmethod
    def draw(self):
        pass
