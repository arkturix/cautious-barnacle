"""Main application file"""
from blackjack.common import exceptions
from blackjack.player import Player
from blackjack.common.exceptions import InvalidInput
import tenacity
import os


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen


class App:

    def __init__(self) -> None:
        self.player = Player()  # Will be a Player object
        self.player_broke = False
        self.player_quit = False

    def _game_over(self):
        """Prints exit message and exits"""
        print("Game Over. Goodbye!")
        exit()

    def _is_player_broke(self):
        """Determine if player is broke"""
        return self.player.wallet > 0

    def run(self):
        clear()
        self.title_screen()
        self.start_game()
        while not self.player_broke and not self.player_quit:
            try: 
                starting_bet = self._get_starting_bet()
            except tenacity.RetryError:
                print("Failed to get starting bet...")
                self._game_over
            self.player.deal(init_bet=starting_bet)

    def title_screen(self):
        print("!!!\t\tPython Blackjack\t\t!!!")

    def start_game(self):
        """Initialize Player object"""
        try:
            num_decks = self._get_num_decks()
        except tenacity.RetryError:
            print("Failed to get a number of decks...")
            self._game_over()
        self.player = Player(num_of_decks=num_decks)
        print(f"We'll play with {num_decks} decks of cards.")

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(InvalidInput),
        stop=tenacity.stop_after_attempt(3)
    )
    def _get_num_decks(self) -> int:
        """Get the number of decks desired"""
        num_decks = input("How many decks would you like to play with?")
        if type(num_decks) != int:
            raise InvalidInput("Decks must be a number!")
        elif num_decks < 1 or num_decks > 8:
            raise InvalidInput("Number of decks must be between 1 and 8.")
        else:
            return num_decks

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(InvalidInput),
        stop=tenacity.stop_after_attempt(3)
    )
    def _get_starting_bet(self) -> int:
        """Get the starting bet for a round"""
        bet_amount = input("How much would you like to start betting this round?")
        if type(bet_amount) != int:
            raise InvalidInput("Bet amount must be a number")
        else:
            return bet_amount
