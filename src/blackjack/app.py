"""Main application file"""
from blackjack.player import Player
from blackjack.common.exceptions import InvalidInput, IllegalBet
import tenacity
import os
import time


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen


class App:

    def __init__(self) -> None:
        self.player = None  # Will be a Player object
        self.player_quit = False
        self.quit_actions = ['q', 'quit']

    def _game_over(self):
        """Prints exit message and exits"""
        print("Game Over. Goodbye!")
        exit()

    def _is_player_broke(self):
        """Determine if player is broke"""
        return self.player.wallet.balance < 0

    @property
    def player_broke(self):
        return self._is_player_broke()

    def _set_player_quit(self):
        """Set the player quit flag"""
        self.player_quit = not self.player_quit

    def run(self):
        clear()
        self.title_screen()
        self.start_game()
        time.sleep(1)
        while not self.player_broke and not self.player_quit:
            clear()
            print("Let's play!")
            try:
                self._deal()
            except IllegalBet:
                print("Failed to get valid initial bet...")
                self._game_over()
            player_bust = False
            round_counter = 1
            time.sleep(1)
            while not self.player._is_standing and not player_bust and not self.player_broke and not self.player_quit:
                clear()
                print(f"Your current bet: ${self.player.current_bet}")
                # Show dealer card
                self._dealer_display_card()
                # Show player cards
                self._player_display_cards()
                # Prompt user for action: bet, hit, double, split, surrender, stand
                try:
                    action = self._prompt_player_action()
                except InvalidInput:
                    print("Failed to get a valid action...")
                    self._game_over()
                self._do_action(action=action, round=round_counter)
                if self.player.hand.total() > 21:
                    player_bust = True
                round_counter += 1
                time.sleep(1)
            if self.player_quit:
                self._game_over()
            if player_bust:
                self._player_bust()
            else:
                dealer_bust = False
                while not dealer_bust and self.player.dealer.hand.total() < 17:
                    clear()
                    print(f"Your current bet: ${self.player.current_bet}")
                    # Show dealer cards
                    self._dealer_display_cards()
                    self._player_display_cards()
                    # Dealer draws
                    self.player.dealer.draw()
                    if self.player.dealer.hand.total() > 21:
                        dealer_bust = True
                    time.sleep(1)
                # Dealer busts
                if dealer_bust:
                    self._dealer_bust()
                # Determine winner
                self._determine_winner()
            # Resolve round
            response = input("Continue?")
            if response.lower() in self.quit_actions:
                self._set_player_quit()
            self.player.resolve_round()
            self.player.dealer.resolve()
        if self.player_broke:
            print("You're broke!!!")
        self._game_over()

    def title_screen(self):
        print("!!!\t\tPython Blackjack\t\t!!!")

    def start_game(self):
        """Initialize Player object"""
        try:
            num_decks = self._get_num_decks()
        except InvalidInput:
            print("Failed to get a number of decks...")
            self._game_over()
        self.player = Player(num_of_decks=num_decks)
        print(f"We'll play with {num_decks} decks of cards.")

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(InvalidInput),
        stop=tenacity.stop_after_attempt(3),
        reraise=True
    )
    def _get_num_decks(self) -> int:
        """Get the number of decks desired"""
        num_decks = input("How many decks would you like to play with?\n")
        try:
            num_decks = int(num_decks)
        except ValueError:
            raise InvalidInput("Decks must be a number!")
        if num_decks < 1 or num_decks > 8:
            raise InvalidInput("Number of decks must be between 1 and 8.")
        else:
            return num_decks

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(InvalidInput),
        stop=tenacity.stop_after_attempt(3),
        reraise=True
    )
    def _get_starting_bet(self) -> int:
        """Get the starting bet for a round"""
        bet_amount = input(f"How much would you like to start betting this round? Min $10. You currently have ${self.player.wallet.balance}\n")
        try:
            bet_amount = int(bet_amount)
        except ValueError:
            raise InvalidInput("Bet amount must be a number.")
        else:
            return bet_amount

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(IllegalBet),
        stop=tenacity.stop_after_attempt(3),
        reraise=True
    )
    def _deal(self):
        try: 
            starting_bet = self._get_starting_bet()
            self.player.deal(init_bet=starting_bet)
        except InvalidInput:
            print("Failed to get starting bet...")
            self._game_over()

    def _dealer_display_card(self):
        """Display dealer's initial card"""
        dealer_initial_card_str = f"\nDealer shows:\n\n    {self.player.dealer.display_card[0]} of {self.player.dealer.display_card[1]}\n    and a hole card, face-down.\n\n"
        print(dealer_initial_card_str)

    def _dealer_display_cards(self):
        """Display all of the dealer's cards"""
        dealer_cards_str = "\nDealer hand is:\n\n"
        for card in self.player.dealer.hand.cards:
            dealer_cards_str += f"    {card[0]} of {card[1]}\n"
        dealer_cards_str += f"\nDealer hand has a value of {self.player.dealer.hand.total()}"
        print(dealer_cards_str)

    def _player_display_cards(self):
        player_cards_str = "\nYour hand is:\n\n"
        for card in self.player.hand.cards:
            player_cards_str += f"    {card[0]} of {card[1]}\n"
        player_cards_str += f"\nYour hand has a value of {self.player.hand.total()}"
        print(player_cards_str)

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(InvalidInput),
        stop=tenacity.stop_after_attempt(3),
        reraise=True
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
        # Bet on split
        split_bet_actions = ['sb', 'split bet']
        # Surrender
        surrender_actions = ['su', 'surrender']
        # Stand
        stand_actions = ['st', 'stand']
        all_actions = bet_actions + hit_actions + double_actions + split_actions + surrender_actions + stand_actions + self.quit_actions
        
        player_action = input("What would you like to do? ({})\n".format(', '.join(all_actions[1::2])))
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
            elif player_action.lower() in split_bet_actions:
                return 'split bet'
            elif player_action.lower() in surrender_actions:
                return 'surrender'
            elif player_action.lower() in stand_actions:
                return 'stand'
            elif player_action.lower() in self.quit_actions:
                return 'quit'

    def _do_action(self, action, round):
        """Run function associated with action"""
        if action in ['split', 'surrender'] and round != 1:
            print(f"Cannot {action} after the first round.")
            return None
        actions = {
            'bet': self._round_bet,
            'hit': self.player.hit,
            'double': self.player.double,
            'split': self._split_hand,
            'split bet': self._bet_split,
            'surrender': self.player.surrender,
            'stand': self.player.stand,
            'quit': self._set_player_quit
        }
        return actions[action]()

    @tenacity.retry(
        retry=(tenacity.retry_if_exception_type(InvalidInput) | tenacity.retry_if_exception_type(IllegalBet)),
        stop=tenacity.stop_after_attempt(3)
    )
    def _get_round_bet(self):
        """Get bet during round"""
        bet_amount = input("How much would you like to bet?\n")
        try:
            bet_amount = int(bet_amount)
        except ValueError:
            raise InvalidInput("Bet amount must be a number.")
        else:
            return bet_amount

    def _round_bet(self):
        """Update current bet"""
        try:
            bet_amt = self._get_round_bet()
        except tenacity.RetryError:
            print("Could not get a valid bet amount...")
            self._game_over()
        self.player.bet(bet_amt)

    @tenacity.retry(
        retry=(tenacity.retry_if_exception_type(InvalidInput) | tenacity.retry_if_exception_type(IllegalBet)),
        stop=tenacity.stop_after_attempt(3)
    )
    def _get_split_bet(self):
        """Get split bet"""
        bet_amount = input("How much would you like to bet on the split?\n")
        try:
            bet_amount = int(bet_amount)
        except ValueError:
            raise InvalidInput("Bet amount must be a number.")
        else:
            return bet_amount

    def _split_hand(self):
        """Split the hand"""
        try:
            bet_amt = self._get_split_bet()
        except tenacity.RetryError:
            print("Could not get a valid bet amount...")
            self._game_over()
        self.player.split(bet_amt)

    def _bet_split(self):
        """Bet on the split hand"""
        try:
            bet_amt = self._get_split_bet()
        except tenacity.RetryError:
            print("Could not get a valid bet amount...")
            self._game_over()
        self.player.bet_split(bet_amt)

    def _player_bust(self):
        """Inform player of bust"""
        clear()
        print(f"Your current bet: ${self.player.current_bet}")
        self._dealer_display_cards()
        self._player_display_cards()
        print("!!!\tBUST\t!!!")
        self._player_lose()

    def _player_lose(self):
        """Inform player of loss"""
        print("You lost this hand.")
        self.player.wallet - self.player.current_bet
        print(f"You lost ${self.player.current_bet}. You have ${self.player.wallet.balance} remaining.")

    def _player_win(self):
        """Inform player of win"""
        print("You won this hand!")
        self.player.wallet + self.player.current_bet
        print(f"You won ${self.player.current_bet}. You have ${self.player.wallet.balance} remaining.")

    def _dealer_bust(self):
        """Inform player of dealer bust"""
        clear()
        print(f"Your current bet: ${self.player.current_bet}")
        self._dealer_display_cards()
        self._player_display_cards()
        print("!!!\tDEALER BUST\t!!!")
        self._player_win()

    def _determine_winner(self):
        """Determine winner"""
        clear()
        print(f"Your current bet: ${self.player.current_bet}")
        self._dealer_display_cards()
        self._player_display_cards()
        if self.player.hand.total() > self.player.dealer.hand.total():
            self._player_win()
        else:
            self._player_lose()
