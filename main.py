from exceptions import *
from ships import *
from globals import *

class Player:
    def __init__(self):
        self.board = Board()
        self.score = NUM_SHIPS

    def get_board(self) -> int:
        """
            Returns the score of the player
            Parameters: 
                None
            Return: 
                score (int): The score of the player 
        """
        return self.score

    def print_board(self) -> None:
        """
            Calls the print_board function in the Board class
            Parameters: 
                None
            Return: 
                None 
        """
        self.board.print_board()

    def print_ship_status(self) -> None:
        """
            Calls the print_ship_status function in the Board class
            Parameters: 
                None
            Return: 
                None 
        """
        self.board.print_ship_status()
        
    def fire(self, position: str) -> None:
        """
            Calls the fire function in the Board class, updates score
            Parameters: 
                position (str): Position to be hit on the board. Formatted as <Letter><Number>.
            Return: 
                None 
        """
        self.score -= self.board.fire(position)

class Board:
    def __init__(self):
        self.board = {}
        self.ship_status = [0]*NUM_TYPE_SHIPS
        self.initialize_board()

    
    def initialize_board(self) -> None:
        """
            Receives user input to place the ships on board in the beginning of the game
            Parameters: 
                None
            Return: 
                None 
        """
        for i in range(NUM_SHIPS):
            while True:
                try:
                    # Receive user input
                    command, ship_name, direction, position, *_ = input().strip().split()

                    # Place ship on board based on size and type
                    if command == "PLACE_SHIP":
                        if ship_name == "Carrier":
                            self.place_ship(Ship_Carrier.size, Ship_Carrier.id, direction, position)     
                        elif ship_name == "Battleship":
                            self.place_ship(Ship_Battleship.size, Ship_Battleship.id, direction, position)
                        elif ship_name == "Cruiser":
                            self.place_ship(Ship_Cruiser.size, Ship_Cruiser.id, direction, position)
                        elif ship_name == "Submarine":
                            self.place_ship(Ship_Submarine.size, Ship_Submarine.id, direction, position)
                        elif ship_name == "Destroyer":
                            self.place_ship(Ship_Destroyer.size, Ship_Destroyer.id, direction, position)
                        else:
                            raise ShipTypeInputError
                    elif command == "FIRE":
                        raise FireCommandError
                    else: 
                        raise CommandInputError

                # Error check
                except GameExceptions as e:
                    print(e)
                    continue
                except ValueError as e:
                    print("Invalid input.")
                    continue
                else:
                    break

    def fire(self, position: str) -> int:
        """
            Validates position, then fires at the position on the board. If it hits a ship,
            it removes the ship piece from the board, and updates the score if it sinks the ship.
            Parameters: 
                position (str): Position to be hit on the board. Formatted as <Letter><Number>.
            Return: 
                None 
        """
        
        # Verify that the position is formatted as <Letter><Number>
        if position[0].isalpha() and position[1:].isnumeric():
            pos_x = ord(position[0].upper())-64
            pos_y = int(position[1:])

            # Verify that the position is on the board
            if pos_x < 1 or pos_y < 1 or pos_x > BOARD_SIZE or pos_y > BOARD_SIZE:
                raise positionInputError
        else:
            raise positionInputError
        
        # Check if ship is in position
        if (pos_x,pos_y) in self.board:
            print("Hit")
            ship_type = self.board[(pos_x,pos_y)]
            self.ship_status[ship_type] -= 1 
            del self.board[(pos_x,pos_y)]

            # Check if ship is sunk, return 1 to subtract from score
            if self.ship_status[ship_type] == 0:
                print("You sunk my {}!".format(ship_name_index[ship_type]))
                return 1
        else:
            print("Miss")
        
        return 0

    def place_ship(self, ship_size: int, ship_type: int, direction: str, position: str) -> None:
        """
            Validates the position and direction received from user. Places ship on board.
            Parameters: 
                ship_size (int): The size of the ship to be placed.
                ship_type (int): The id of the ship to be placed.
                direction (str): Direction to place ship in. Formatted as "down" or "right".
                position (str): Position to be hit on the board. Formatted as <Letter><Number>.
            Return: 
                None 
        """
        if self.ship_status[ship_type] != 0:
            raise MaxShipError
            
        # Verify that the position and direction are available on the board
        try:
            if position[0].isalpha() and position[1:].isnumeric():
                pos_x = ord(position[0].upper())-64
                pos_y = int(position[1:])
            else:
                raise positionInputError
            self.verify_positions(pos_x,pos_y,direction,ship_size)

        # Error check
        except (IndexError, TypeError, ValueError):
            raise positionInputError
        
        # Save the ship ID into the position
        if direction == "down":
            for i in range(ship_size):
                self.board[(pos_x+i,pos_y)] = ship_type
        else:
            for i in range(ship_size):
                self.board[(pos_x,pos_y+i)] = ship_type

        self.ship_status[ship_type] = shiPp_size
        print("Placed {}".format(ship_name_index[ship_type]))

    def verify_positions(self, pos_x: int, pos_y: int, direction: str, ship_size: int) -> None:
        """
            Validates the position and direction received from user. Places ship on board.
            Parameters: 
                ship_size (int): The size of the ship to be placed.
                ship_type (int): The id of the ship to be placed.
                direction (str): Direction to place ship in. Formatted as "down" or "right".
                position (str): Position to be hit on the board. Formatted as <Letter><Number>.
            Return: 
                None 
        """
        # Verify that the position is on the board
        if pos_x < 1 or pos_y < 1 or pos_x > BOARD_SIZE or pos_y > BOARD_SIZE:
                raise BoardIndexError
        
        # Verify that the positions in the given direction are on the board
        if direction == "down":
            if pos_x+ship_size > BOARD_SIZE:
                raise BoardIndexError
            for i in range(ship_size):
                if (pos_x+i,pos_y) in self.board:
                    raise ShipCollisionError            
        elif direction == "right":
            if pos_y+ship_size > BOARD_SIZE:
                raise BoardIndexError
            for i in range(ship_size):
                if (pos_x,pos_y+i) in self.board:
                    raise ShipCollisionError
        else:
            raise DirectionInputError

    def print_board(self) -> None:
        """
            Prints board to standard out as a table.
            Parameters: 
                None
            Return: 
                None 
        """
        # Print first line
        print("  ", end="")
        for i in range(1,BOARD_SIZE+1):
            if i < 10:
                print("| {} ".format(i),end="")
            else:
               print("| {}".format(i),end="") 
        print("|")

        # Print rest of board
        for pos_x in range(1,BOARD_SIZE+1):
            print("{} ".format(chr(pos_x+64)),end="")
            for pos_y in range(1,BOARD_SIZE+1):
                if (pos_x,pos_y) in self.board:
                    print("| {} ".format(self.board[(pos_x,pos_y)]),end="")
                else:
                    print("|___",end="")
            print("|")

    def print_ship_status(self) -> None:
        """
            Prints the ship status to standard out as a list
            Parameters: 
                None
            Return: 
                None 
        """
        print(self.ship_status)

def play_game():
    """
        Initiates the game. Creates two players each with their own board. Fills both boards 
        with ships from user input. Then, fires shots to each board based on user input from
        each player. Ends the game once one of the scores reaches 0.
        Parameters: 
            None
        Return: 
            None 
    """
    # Initialize the board for player 1
    print("Player 1:")
    player_1 = Player()

    # Initialize the board for player 2
    print("Player 2:")
    player_2 = Player()

    
    curr_player = 1
    while True:
        try:
            # Receive user input for FIRE command
            print("Player {}: ".format(curr_player),end="")
            command, position, *_ = input().strip().split()

            # Call FIRE, switch player
            if command == "PLACE_SHIP":
                raise PlaceShipCommandError
            if curr_player == 1:
                player_2.fire(position)
                curr_player = 2
            else:
                player_1.fire(position)
                curr_player = 1

        # Error check
        except GameExceptions as e:
            print(e)
            continue
        except ValueError:
            print("Invalid input.")
            continue

        # Check score and exit
        if player_1.score == 0 or player_2.score == 0:
            print("Game over.")
            break

if __name__ == "__main__":
    """
    Entry point.
    """
    play_game()