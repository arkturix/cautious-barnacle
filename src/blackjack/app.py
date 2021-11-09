"""Main application file"""
from blackjack import player
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
            clear()
            print("Let's play!")
            try: 
                starting_bet = self._get_starting_bet()
            except tenacity.RetryError:
                print("Failed to get starting bet...")
                self._game_over()
            self.player.deal(init_bet=starting_bet)
            player_bust = False
            round_counter = 1
            while not self.player._is_standing and not player_bust:
                clear()
                print(f"Your current bet: {self.player.current_bet}")
                # Show dealer card
                self._dealer_display_card()
                # Show player cards
                self._player_display_cards()
                # Prompt user for action: bet, hit, double, split, surrender, stand
                # Repeat until either hold or bust
                try:
                    action = self._prompt_player_action()
                except tenacity.RetryError:
                    print("Failed to get a valid action...")
                    self._game_over()
            # Show dealer cards
            # Dealer draws
            # Determine winner
            # Resolve round

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

    def _dealer_display_card(self):
        """Display dealer's initial card"""
        dealer_initial_card_str = f"""
        Dealer shows:
        
            {self.player.dealer.display_card[0]} of {self.player.dealer.display_card[1]}
            and hole card, face-down.
        
        """
        print(dealer_initial_card_str)

    def _player_display_cards(self):
        player_cards_str = f"""
        Your hand is:

        """
        for card in self.player.hand.cards:
            player_cards_str += f"    {card[0]} of {card[1]}\n"
        player_cards_str += f"Your hand has a value of {self.player.hand.total()}"

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(InvalidInput),
        stop=tenacity.stop_after_attempt(3)
    )
    def _prompt_player_action(self) -> str:
        """Prompt player for action during round"""
        # Bet
        bet_actions = ['b', 'bet']
        # Hit
        hit_actions = ['h', 'hit']
        # Double
        double_actions = ['d', 'double']
        # Split
        split_actions = ['sp', 'split']
        # Surrender
        surrender_actions = ['su', 'surrender']
        # Stand
        stand_actions = ['st', 'stand']
        all_actions = bet_actions + hit_actions + double_actions + split_actions + surrender_actions + stand_actions
        
        player_action = input("What would you like to do?")
        if player_action.lower() not in all_actions:
            raise InvalidInput(f"You entered {player_action}, this is not a valid action.")
        else:
            if player_action.lower() in bet_actions:
                return 'bet'
            elif player_action.lower() in hit_actions:
                return 'hit'
            elif player_action.lower() in double_actions:
                return 'double'
            elif player_action.lower() in split_actions:
                return 'split'
            elif player_action.lower() in surrender_actions:
                return 'surrender'
            elif player_action.lower() in stand_actions:
                return 'stand'
