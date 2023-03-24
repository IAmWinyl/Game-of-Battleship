# Exceptions
class GameExceptions(Exception):
    pass

class CommandInputError(GameExceptions):
    def __init__(self):
         super().__init__("Invalid command.")

class FireCommandError(GameExceptions):
    def __init__(self):
         super().__init__("Cannot fire before placing all ships.")

class PlaceShipCommandError(GameExceptions):
    def __init__(self):
         super().__init__("Cannot place any more ships.")

class ShipTypeInputError(GameExceptions):
    def __init__(self):
         super().__init__("Invalid ship type.")

class positionInputError(GameExceptions):
    def __init__(self):
         super().__init__("Invalid position.")
    
class BoardIndexError(GameExceptions):
    def __init__(self):
         super().__init__("Ship cannot be placed off the board.")

class ShipCollisionError(GameExceptions):
    def __init__(self):
         super().__init__("One or more tiles in this direction are unavailable.")

class DirectionInputError(GameExceptions):
    def __init__(self):
         super().__init__("Invalid direction")

class MaxShipError(GameExceptions):
    def __init__(self):
         super().__init__("Out of available ships of this type.")
