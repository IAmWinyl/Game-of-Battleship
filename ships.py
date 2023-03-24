from abc import (
  ABC,
  abstractmethod,
)

# Abstract classes
class Ship(ABC):
    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

# Ship types
class Ship_Carrier(Ship):
    id = 0
    size = 5

class Ship_Battleship(Ship):
    id = 1
    size = 4

class Ship_Cruiser(Ship):
    id = 2
    size = 3

class Ship_Submarine(Ship):
    id = 3
    size = 3

class Ship_Destroyer(Ship):
    id = 4
    size = 2

ship_name_index = {
    0: "Carrier",
    1: "Battleship",
    2: "Cruiser",
    3: "Submarine",
    4: "Destroyer",
}