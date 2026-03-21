# Not fully implemented and complete

# Though this was not necessary, ill still attatch it as I had
# made an attempt to make it work


# ------------------------------------------------------#
#                     Card class                        #
# This class is used to represent a single playing card #
# ------------------------------------------------------#

class Card:
    # These are the class variables that are shared by all card instances, not necessarily stored per card
    # every card within the deck uses the same possible ranks & suits, so theres no reason to copy these lists on each obj
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def __init__(self, rank, suit, plastic=False):
        # the rank will appear as one of the strings within the ranks list
        self.rank = rank
        # the suit will appear as one of the strings within the suits list
        self.suit = suit
        # This value will be true only for the special card, and false for all real cards
        # with the default being false, that means that the normal Card (rank, suit) calls
        # do not need to mention it, only the one plastic card is ever set as true
        self.plastic = plastic

    def val(self):
        # This function will return the numeric value of the card,
        # i.e. face cards have a val of 10 and an ace can be 1 or 11
        # depending on what is at play

        # First and foremost, the plastic card, it is not a real card and
        # has no game value, so its value is 0
        if self.plastic:
            return 0

        # Face cards, this is the Jack, Queen, and King. In bj they are 10.
        if self.rank in ('Jack', 'Queen', 'King'):
            return 10

        # Ace is 11 by default, unless the value exceeds 21, then the hand will
        # reduce its value to 1 as needed
        if self.rank == 'Ace':
            return 11

        # The number cards will simply be their respective val, the only note is that
        # as these are stored as strings in a list, they must be converted to an integer val
        return int(self.rank)

    def __repr__(self):
        # As introduced ~lecture 10, the repr function is a dunder method to represent an
        # unambiguous string representation of an object
        # This will control what we see when printing a card, w/o this we would see the address

        # The plastic card will have its own identification as it will cause a reshuffle
        if self.plastic:
            return '[Plastic]'

        # As for the rest of the cards, they will be displayed as their "rank" of "suit"
        return f'{self.rank} of {self.suit}'


# -------------------------------------------------------#
#                      Deck class                        #
# represents the decks in blackjack, this class handles  #
# multiple decks being present as is standard with       #
# most casinos, winstar is 6 so we will use 6 decks here #
# -------------------------------------------------------#

class Deck:
    def __init__(self, n_decks=6):
        # n_decks is the number of decks, it will dictate how many 52-card decks will be combined.
        # Local casinos all use 6, as this is the standard in Oklahoma
        self.n_decks = n_decks

        # This concerns the reshuffle, whenever the plastic card is drawn this value will become
        # true and call for a reshuffle. Base value is false, deck creation will not call for a reshuffle
        self.reshuffle = False

        # This will call for the build and shuffle of the deck. In blackjack, the term may also be
        # called 'washing the deck', this method is used to maximize randomness of decks within a
        # shoe, useful when cards are considered 'sticky' from a previous play or when dishing out
        # a new deck
        self.wash()

    def wash(self):
        # This function will build the card list using a list comprehension. Nested loops are
        # utilized to create one card per rank & suit combination. This will be repeated n_decks
        # times, in this case it is 6 x 52 = 312 cards total.
        self.cards = [
            Card(rank, suit)
            for i in range(self.n_decks)  # repeat each deck
            for suit in Card.suits        # iterate over all 4 suits
            for rank in Card.ranks        # iterate over all 13 ranks
        ]

        # shuffle the list, this will randomize the order of all 312 cards
        random.shuffle(self.cards)

        # Insert the plastic card, in context this is the cut card that determines the shuffle
        # point. The cut card will be at a random position in the middle third of the entire shoe.
        # Ideally, the shoe will be between 33% and 66% used before triggering a reshuffle.
        total = len(self.cards)
        plastic_cutcard = random.randint(total // 3, 2 * total // 3)
        self.cards.insert(plastic_cutcard, Card('Plastic', 'Plastic', plastic=True))

        # reset plastic back to false after the shoe is rebuilt after a reshuffle
        self.reshuffle = False

    def shuffle(self):
        # just calls back to wash for shuffling
        self.wash()

    def draw(self):
        # This function calls and returns the top card from the shoe, in context this means that
        # it is pulling the last item from the list and treating this as the top of the deck.
        # the list.pop() python utility removes and returns the last element.
        if not self.cards:
            self.wash()

        # remove and return last card in list, in other words, the top of the deck
        card = self.cards.pop()

        # If the plastic card is drawn, set the reshuffle flag to true and draw the actual card
        # sitting behind it. The plastic card is never returned, it is only a marker
        if card.plastic:
            self.reshuffle = True

            # safety net if plastic is very last item
            if not self.cards:
                self.wash()

            # draw real card sitting behind plastic marker
            card = self.cards.pop()

        return card

    def cards_left(self):
        # returns how many cards are left in the shoe
        return len(self.cards)

    def __repr__(self):
        # as before, this is an f string giving a readable summary of the deck obj
        return f'Deck({self.n_decks} decks, {self.cards_left()} cards remaining)'


# ---------------------------------------------------#
#                   Hand Class                       #
# The set of cards held by one player or the dealer  #
# during a single round. Responsible for knowing     #
# its own total value & whether it has bust          #
# ---------------------------------------------------#

class Hand:
    def __init__(self):
        # cards: the list of card obj currently in hand
        self.cards = []

    def hit(self, card):
        # adds a card to the hand, functions as a "hit"
        self.cards.append(card)

    def val(self):
        # This computes the best total value without busting, start by summing all card values
        # using the val() method from the class Card
        total = sum(card.val() for card in self.cards)

        # As outlined by the skeleton prior, count aces in hand and determine whether the value
        # shall represent 11 as it does by default, or if we need to shrink it to 1. We do this
        # ace by ace until we are under 21 or every ace has been reduced.
        aces = sum(1 for card in self.cards if card.rank == 'Ace')

        # subtract by 10 to reduce ace to 1
        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def bust(self):
        # self explanatory, this function will return true if the val exceeds 21
        return self.val() > 21

    def blackjack(self):
        # returns true if exactly 2 cards total to 21
        # for further clarification, a 21 from 3 cards would not qualify
        return len(self.cards) == 2 and self.val() == 21

    def clear(self):
        # empties hand between rounds, hence the name
        self.cards = []

    def __repr__(self):
        # as before, this is the printed result
        return f'{self.cards} = {self.val()}'


# ------------------------------------------------------------------#
#                    Player class                                   #
# This is the base class, and subclasses will be implemented later  #
# ------------------------------------------------------------------#

class Player:
    def __init__(self, name, chips=500):
        # rather than going by chip type, for the sake of this lab, we will simply refer
        # to the chips total monetary value
        self.name = name
        self.chips = chips
        self.hand = Hand()
        self.bet = 0

    def place_bet(self, cards_viewed):
        # Base class just returns a flat default bet & subclasses will override this with
        # different logic, we use min() so a player cannot bet more than they currently have
        return min(10, self.chips)

    def choice(self, dealer_up, cards_viewed):
        # in this context, dealer_up refers to the card from the dealer that is visible
        # this function is the one allowing for the choice between hit or stand
        # For this instance, the player will always stand by default, subclasses with
        # strategies will differ
        return 'stand'

    def receive(self, card):
        # this adds the dealt card to the hand
        self.hand.hit(card)

    def __repr__(self):
        # displays name and chip total
        return f'{self.name} (${self.chips})'


# -------------------------------------------------------#
#                   Dealer class                         #
# Subclass of Player, same structure, fixed decisions    #
# -------------------------------------------------------#

class Dealer(Player):

    def __init__(self):
        # Calls Player.__init__ for hand setup, no chips or real bet needed
        # super() is utilized to access properties from a parent or sibling class,
        # in this case the dealer class is accessing properties from the Player class.
        # As expected, the dealer chips will be 0 because the dealer does not play
        super().__init__(name='Dealer', chips=0)

    def choice(self, dealer_up, cards_viewed):
        # Hit on 16 or under, stand on 17+, this is the standard dealers rule
        # Ignores cards_viewed and dealer_up entirely
        if self.hand.val() <= 16:
            return 'hit'
        return 'stand'

    def up_card(self):
        # Returns the face-up card that the players can see
        # the first card dealt to dealer is the face up card, and it will
        # return None if no cards have yet been dealt as a safety check
        if self.hand.cards:
            return self.hand.cards[0]
        return None


# -------------------------------------------------------#
#                  Human Player                          #
# This is the subclass of player for an interactive      #
# human at the table, interactions come from user input  #
# -------------------------------------------------------#

class HumanPlayer(Player):

    def __init__(self, name, chips=500):
        # Pass straight up to Player's __init__ using the same super() as seen before
        super().__init__(name, chips)

    def place_bet(self, cards_viewed):
        # Ask the user how much they want to bet and keep asking until they give a valid number
        # TryExcept is used for error checking
        while True:
            try:
                amount = int(input(f'{self.name} (${self.chips}) — enter bet: $'))
                if 1 <= amount <= self.chips:
                    return amount
                # If the number is valid but out of range, explain why
                print(f'  Bet must be between $1 and ${self.chips}')
            except ValueError:
                # If they typed something that isn't a number at all
                print('  Please enter a number')

    def choice(self, dealer_up, cards_viewed):
        # Show the player what they're working with, then ask hit or stand
        print(f'  Your hand : {self.hand}')
        print(f'  Dealer shows : {dealer_up}')
        while True:
            action = input('  Hit or stand? (h/s): ').strip().lower()
            if action in ('h', 'hit'):
                return 'hit'
            if action in ('s', 'stand'):
                return 'stand'
            print('  Please enter h or s')


# -------------------------------------------------------#
#                DealerStrategyPlayer                    #
# A computer player that mirrors the dealers strategy,   #
# hit on 16 or under, stand on 17 or over, flat bet      #
# -------------------------------------------------------#

class DealerStrategyPlayer(Player):

    def __init__(self, name, chips=500):
        # passes straight up to Player init, nothing extra needed
        super().__init__(name, chips)

    def place_bet(self, cards_viewed):
        # flat bet every round, never more than what they have
        return min(10, self.chips)

    def choice(self, dealer_up, cards_viewed):
        # mirrors the dealer exactly, hit on 16 or under
        if self.hand.val() <= 16:
            return 'hit'
        return 'stand'


# -------------------------------------------------------#
#                   HiLoPlayer                           #
# This player uses the Hi-Lo card counting strategy,     #
# tracking the running count of all cards seen so far    #
# to make smarter betting and hit/stand decisions        #
# -------------------------------------------------------#

class HiLoPlayer(Player):

    def __init__(self, name, chips=500, threshold=0):
        # passes name and chips up to Player init as usual
        super().__init__(name, chips)

        # threshold is the count value that determines hit vs stand
        # if the running count is at or above this number, stand
        # if it is below, hit. 0 is the threshold value we will use here
        self.threshold = threshold

    def __running_count(self, cards_viewed):
        # computes the Hi-Lo running count from all cards seen so far
        # this is the core of the counting strategy —
        # low cards (2-6) leaving the deck is good for the player because it means more high
        # cards remain, so we count them as +1. High cards (10-A) leaving is bad for the
        # player, so they are -1. Neutral cards (7-9) do not affect the count
        count = 0
        for card in cards_viewed:
            if 2 <= card.val() <= 6:
                count += 1    # low card seen, deck is getting better
            elif card.val() >= 10:
                count -= 1    # high card seen, deck is getting weaker
            # 7, 8, 9 add nothing to the count
        return count

    def place_bet(self, cards_viewed):
        # bet more when the count is positive because the deck is rich in high cards which
        # favors the player, bet the minimum otherwise. An important distinction vs other
        # strategies, others just bet a flat amount whereas here there are variable bets
        count = self.__running_count(cards_viewed)
        if count >= self.threshold:
            return min(50, self.chips)   # favorable deck, bet big
        return min(10, self.chips)       # unfavorable deck, bet small

    def choice(self, dealer_up, cards_viewed):
        # always stand on 17 or above regardless of the count,
        # this is the same hard floor the dealer uses and is just
        # sensible play no matter what the count says
        if self.hand.val() >= 17:
            return 'stand'

        # below 17, let the count decide. A high positive count means lots of face cards
        # remain in the shoe, which means hitting is risky since we are likely to bust,
        # so we stand when the count is at or above the threshold.
        # A negative count means lots of low cards remain, so hitting is safer and we
        # are more likely to improve our hand
        count = self.__running_count(cards_viewed)
        if count >= self.threshold:
            return 'stand'
        return 'hit'


# https://youtu.be/HeVclniKpHs?si=HfYVmppjkXRsoHTQ
# This is the "perfect basic" strategy

# ---------------------------------------------------------#
#                  BasicStrategyPlayer                     #
# A new player implementing perfect basic strategy         #
# combined with Hi-Lo bet spreading from exercise 6        #
# Basic strategy is the mathematically optimal hit/stand   #
# decision for every hand total vs dealer up card          #
# It was computed by running millions of simulations and   #
# finding which decision produces the best outcome for     #
# every possible scenario. Even casinos allow its use      #
# at the table because the house edge still remains,       #
# it just shrinks to around 0.5% with perfect play         #
# ---------------------------------------------------------#

class BasicStrategyPlayer(Player):

    def __init__(self, name, chips=500):
        # passes name and chips straight up to Player init,
        # nothing extra needed here since all the strategy
        # logic lives in the methods below
        super().__init__(name, chips)

    def __running_count(self, cards_viewed):
        # this is the same Hi-Lo running count from exercise 6,
        # the only difference here is that we use it purely for
        # bet sizing rather than hit/stand decisions, since basic
        # strategy handles those decisions on its own through the
        # lookup tables in __hard_strategy and __soft_strategy
        count = 0
        for card in cards_viewed:
            if 2 <= card.val() <= 6:
                # low card just left the deck, meaning the remaining shoe has a slightly
                # higher ratio of high cards, which is favorable for the player
                count += 1
            elif card.val() >= 10:
                # high card just left the deck, meaning the remaining shoe is getting weaker
                count -= 1
            # cards 7, 8, and 9 are considered neutral and do not affect the count
        return count

    def place_bet(self, cards_viewed):
        # unlike the HiLoPlayer in exercise 6 which only had two bet sizes, this player
        # uses three tiers based on the running count. This more closely mirrors how real
        # card counters actually size their bets in practice, scaling up gradually as the
        # deck becomes more favorable rather than jumping straight from minimum to maximum
        count = self.__running_count(cards_viewed)
        if count >= 2:
            return min(50, self.chips)   # very favorable deck, bet big
        elif count >= 0:
            return min(25, self.chips)   # slightly favorable, bet medium
        return min(10, self.chips)       # unfavorable deck, bet small

    def __is_soft(self):
        # a soft hand is one where an ace is being counted as 11 rather than 1, meaning
        # the hand has flexibility since the ace can flip down to 1 if needed to avoid busting.
        # We detect this by checking two conditions simultaneously: first that the hand actually
        # contains an ace, and second that the current total is 21 or under meaning the ace is
        # still contributing 11 rather than having already been reduced to 1 by val() in Hand
        total_with_ace_high = sum(card.val() for card in self.hand.cards)
        has_ace = any(card.rank == 'Ace' for card in self.hand.cards)
        return has_ace and total_with_ace_high <= 21

    def __hard_strategy(self, total, dealer_val):
        # this is the perfect basic strategy lookup table for hard totals. A hard total is
        # any hand without an ace, or one where the ace is already being counted as 1 to avoid
        # busting. Every decision here is mathematically optimal meaning no other choice produces
        # a better expected outcome over the long run
        # https://www.blackjackapprenticeship.com/blackjack-strategy-charts/

        # always stand on hard 17 or above, hitting risks busting with no realistic chance
        # of improving enough to matter
        if total >= 17:
            return 'stand'

        # always hit on 8 or below, you cannot bust and need to improve significantly
        # to have any realistic chance of beating the dealer
        if total <= 8:
            return 'hit'

        # hard 9 — basic strategy says double vs 3-6, otherwise hit
        # since we have no doubling, we hit in all cases
        if total == 9:
            return 'hit'

        # hard 10 — double vs 2-9, hit vs 10 or ace
        # since we have no doubling, hit in all cases. A total of 10 is very strong
        # for hitting since any face card gives us 20 which beats almost everything
        if total == 10:
            return 'hit'

        # hard 11 — double vs everything except ace, hit vs ace
        # since we have no doubling, hit in all cases. Any ten-value card gives us 21
        if total == 11:
            return 'hit'

        # hard 12 — stand vs dealer 4-6 because those are the weakest dealer up cards
        # and the dealer is statistically very likely to bust trying to reach 17,
        # so we do not risk busting ourselves. Hit vs everything else
        if total == 12:
            return 'stand' if 4 <= dealer_val <= 6 else 'hit'

        # hard 13-16 — stand vs dealer 2-6 (weak dealer), hit vs 7+
        # the logic here is that a dealer showing 2-6 must hit and is statistically
        # likely to bust, so we do not risk busting for ourselves. Vs dealer 7 through
        # ace the dealer is too strong and likely already has a made hand, so we must
        # take the risk of hitting to try to improve
        if 13 <= total <= 16:
            return 'stand' if dealer_val <= 6 else 'hit'

        return 'hit'

    def __soft_strategy(self, total, dealer_val):
        # perfect basic strategy for soft totals. Soft hands are more forgiving than hard
        # hands because the ace can always flip from 11 down to 1 if we draw a high card,
        # meaning we can never actually bust on a single hit from a soft hand

        # soft 19 or above — always stand, already a strong hand
        if total >= 19:
            return 'stand'

        # soft 18 is the most nuanced decision in all of basic strategy.
        # vs dealer 9, 10, or ace we hit because the dealer likely already has us beaten
        # or close to it, and since we cannot bust on a soft hand we should try to improve.
        # vs dealer 2, 7, or 8 we stand since 18 is strong enough that we are likely ahead.
        # basic strategy actually says to double vs dealer 3-6 here but since we have no
        # doubling implemented we stand instead, which is the next best play
        if total == 18:
            if dealer_val in (9, 10, 11):
                return 'hit'
            return 'stand'

        # soft 17 or below — always hit, the hand is too weak to stand and we cannot bust
        # since the ace will just flip to 1 making hitting completely safe
        return 'hit'

    def choice(self, dealer_up, cards_viewed):
        total = self.hand.val()

        # get the dealers up card value, defaulting to 10 if somehow None.
        # Jack, Queen, and King all count as 10 for strategy purposes
        dealer_val = dealer_up.val() if dealer_up else 10

        # check if this is a soft hand first and route to the correct strategy table.
        # soft and hard hands have meaningfully different optimal decisions so it is
        # important to use the right one
        if self.__is_soft():
            return self.__soft_strategy(total, dealer_val)
        return self.__hard_strategy(total, dealer_val)


# -------------------------------------------------------#
#                   Game class                           #
# This is the class concerning game functionality        #
# -------------------------------------------------------#

class Game:

    def __init__(self, players, n_decks=6, verbose=True):
        self.players = players

        # creates the shoe using the Deck class, n_decks defaults to 6 as that is
        # the casino standard
        self.deck = Deck(n_decks)

        # one dealer per game, created automatically
        self.dealer = Dealer()

        # cards_viewed is the running list of all face-up cards seen this shoe,
        # players with counting strategies will read this list to make decisions
        self.cards_viewed = []

        # verbose controls whether the game prints commentary, useful to turn off
        # when running large simulations in later exercises
        self.verbose = verbose

        # tracks which round we are on, starts at 0 and increments each round
        self.round_num = 0

    def __log(self, message):
        # this is the central print gate, every message in the game goes through here
        # if verbose is false, nothing prints at all, keeping simulations clean
        if self.verbose:
            print(message)

    # --- Public ------------------------------------------
    # play_round is the only method that should be called from outside the class

    def play_round(self):
        self.round_num += 1
        self.__log(f'\n{"-"*40}')
        self.__log(f'  ROUND {self.round_num}')
        self.__log(f'{"-"*40}')

        # only players who still have chips are allowed to play this round
        active = [p for p in self.players if p.chips > 0]
        if not active:
            self.__log('All players are out of chips.')
            return

        # step 1 — collect bets from all active players
        # chips are deducted here and added back later on a win or push
        for player in active:
            player.bet = player.place_bet(self.cards_viewed)
            player.chips -= player.bet
            self.__log(f'  {player.name} bets ${player.bet}  (${player.chips} remaining)')

        # step 2 — deal the opening two cards to everyone
        self.__deal_initial(active)

        # step 3 — each player takes their turn one at a time
        for player in active:
            self.__log(f'\n  {player.name}\'s turn:')
            self.__player_turn(player)

        # step 4 — dealer takes their turn after all players are done
        self.__log(f'\n  Dealer\'s turn:')
        self.__dealer_turn()

        # step 5 — compare all hands to the dealer and move chips accordingly
        self.__log(f'\n  Results:')
        self.__settle_bets(active)

        # step 6 — clear all hands so everyone starts fresh next round
        self.dealer.hand.clear()
        for player in active:
            player.hand.clear()

        # step 7 — if the plastic card was drawn this round, reshuffle the shoe
        # and reset cards_viewed since the count no longer applies to a new shoe
        if self.deck.reshuffle:
            self.__log('  [Plastic card reached — reshuffling the shoe]')
            self.deck.wash()
            self.cards_viewed = []

    # --- Private -----------------------------------------
    # everything below is internal, only play_round should call these

    def __deal_initial(self, active):
        # this follows the standard casino deal order, one card to each player
        # left to right, then the dealer, then a second card to each player,
        # then the dealers hole card

        # first card to every player, face up so it goes into cards_viewed
        for player in active:
            self.__deal_card(player, face_up=True)

        # dealers first card, this is the up card that everyone can see
        self.__deal_card(self.dealer, face_up=True)

        # second card to every player, also face up
        for player in active:
            self.__deal_card(player, face_up=True)

        # dealers hole card, face down so it does NOT go into cards_viewed yet
        # it gets revealed and recorded later in __dealer_turn
        self.__deal_card(self.dealer, face_up=False)

        self.__log(f'  Dealer shows : {self.dealer.up_card()}')
        for player in active:
            self.__log(f'  {player.name} hand : {player.hand}')

    def __deal_card(self, recipient, face_up=True):
        # draws a card from the shoe and gives it to whoever needs it,
        # this is a helper used by __deal_initial and __player_turn so the
        # draw-and-notify logic only has to live in one place
        card = self.deck.draw()
        recipient.receive(card)

        # only face up cards get added to cards_viewed, the hole card skips this
        if face_up:
            self.__notify_viewed(card)

        return card

    def __player_turn(self, player):
        # keeps asking the player to hit or stand until they bust,
        # get blackjack, or choose to stand
        while True:
            if player.hand.blackjack():
                self.__log(f'  {player.name} has blackjack')
                break
            if player.hand.bust():
                self.__log(f'  {player.name} busts with {player.hand}')
                break

            # pass cards_viewed so counting strategies can use it
            action = player.choice(self.dealer.up_card(), self.cards_viewed)

            if action == 'hit':
                card = self.__deal_card(player, face_up=True)
                self.__log(f'  {player.name} hits -> {card}   hand : {player.hand}')
            else:
                self.__log(f'  {player.name} stands with {player.hand}')
                break

    def __dealer_turn(self):
        # the hole card is now revealed, so we add it to cards_viewed here
        # this is the point where card counters learn what the dealer was hiding
        hole = self.dealer.hand.cards[1]
        self.__notify_viewed(hole)
        self.__log(f'  Dealer reveals hole card : {hole}   hand : {self.dealer.hand}')

        # dealer hits until their own choice() method says stand
        while self.dealer.choice(None, self.cards_viewed) == 'hit':
            card = self.__deal_card(self.dealer, face_up=True)
            self.__log(f'  Dealer hits -> {card}   hand : {self.dealer.hand}')

        if self.dealer.hand.bust():
            self.__log(f'  Dealer busts with {self.dealer.hand}')
        else:
            self.__log(f'  Dealer stands with {self.dealer.hand}')

    def __settle_bets(self, active):
        # compares each players hand to the dealers and moves chips accordingly
        # the bet was already subtracted when it was placed, so returning bet * 2
        # means giving back the original stake plus an equal profit,
        # returning just bet is a push where you get your money back but nothing extra,
        # and returning 0 means the bet is simply gone
        d_val = self.dealer.hand.val()
        d_bust = self.dealer.hand.bust()
        d_bj = self.dealer.hand.blackjack()

        for player in active:
            p_val = player.hand.val()
            p_bust = player.hand.bust()
            p_bj = player.hand.blackjack()
            bet = player.bet

            if p_bust:
                # player busted, bet is already gone
                result = 0
                outcome = 'Busts — loses'

            elif p_bj and d_bj:
                # both have blackjack, this is a push so the bet is returned
                result = bet
                outcome = 'Blackjack push — bet returned'

            elif p_bj:
                # player has blackjack and dealer does not, pays out 3:2
                result = bet + int(bet * 1.5)
                outcome = 'BLACKJACK — wins 3:2'

            elif d_bust:
                # dealer busted and player did not, player wins even money
                result = bet * 2
                outcome = 'Dealer busts — wins'

            elif p_val > d_val:
                # player beats dealer, wins even money
                result = bet * 2
                outcome = f'{p_val} vs {d_val} — wins'

            elif p_val == d_val:
                # tie, push, bet is returned
                result = bet
                outcome = f'{p_val} vs {d_val} — push'

            else:
                # dealer wins, bet is gone
                result = 0
                outcome = f'{p_val} vs {d_val} — loses'

            player.chips += result
            net = result - bet
            self.__log(f'  {player.name}: {outcome}  (${net:+})  chips=${player.chips}')

    def __notify_viewed(self, card):
        # adds a face up card to the cards_viewed list, any player using a
        # counting strategy will read this list when making their decisions
        self.cards_viewed.append(card)