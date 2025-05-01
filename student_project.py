
import requests

# Fetch a new deck of cards from the API
def get_new_deck():
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
    response = requests.get(url).json()
    return response["deck_id"]


# Draw cards from the deck
def draw_cards(deck_id, count=2):
    url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=" + str(count)
    response = requests.get(url).json()
    return response["cards"]


# Calculate the total value of a hand
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card["value"] in ["KING", "QUEEN", "JACK"]:
            value += 10
        elif card["value"] == "ACE":
            aces += 1
            value += 11  # Assume Ace is 11 initially
        else:
            value += int(card["value"])

    # Adjust for Aces if total exceeds 21
    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value


# Handle user sign-up
def sign_up(usernames, passwords, balances):
    new_username = input("Create a username: ")
    if new_username in usernames:
        print("That username is taken, please try again.")
        return

    new_password = input("Create a password: ")
    if new_password in passwords:
        print("That password is taken, please try again.")
        return

    usernames.append(new_username)
    passwords.append(new_password)
    balances.append(50)  # Initialize new account with $50
    print(new_username + " registered successfully! $50 has been added to your account.")


# Handle user login
def login(usernames, passwords, balances):
    username = input("Enter your username: ")
    if username not in usernames:
        print("That username does not exist. Please try again.")
        return None, None

    password = input("Enter your password: ")
    if password not in passwords:
        print("That password is incorrect. Please try again.")
        return None, None

    index = usernames.index(username)
    return index, balances[index]


# Main game logic with betting
def play_blackjack(index, usernames, passwords, balances):
    deck_id = get_new_deck()

    # Display the player's current balance
    current_balance = balances[index]
    print("Your current balance is: $" + str(current_balance))

    # Prompt the player to place a bet
    while True:
        try:
            bet = int(input("How much would you like to bet? "))
            if bet > current_balance:
                print("You cannot bet more than your current balance!")
            elif bet <= 0:
                print("Bet must be greater than 0!")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    # Deduct the bet from the balance
    current_balance -= bet
    print("You placed a bet of $" + str(bet) + ". Remaining balance: $" + str(current_balance))

    # Initial card draw
    player_hand = draw_cards(deck_id, count=2)
    dealer_hand = draw_cards(deck_id, count=2)
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    # Display player's initial hand
    print("\nYour initial hand:")
    for card in player_hand:
        print(card["value"] + " of " + card["suit"])
    print("Hand value: " + str(player_value))

    # Player's turn
    while player_value < 21:
        choice = input("\nHit or stand? (h/s): ").lower()
        if choice == 'h':
            new_card = draw_cards(deck_id, count=1)[0]
            player_hand.append(new_card)
            player_value = calculate_hand_value(player_hand)
            print("You drew: " + new_card["value"] + " of " + new_card["suit"])
            print("Your hand now:")
            for card in player_hand:
                print(card["value"] + " of " + card["suit"])
            print("Hand value: " + str(player_value))
        elif choice == 's':
            print("You chose to stand.")
            break
        else:
            print("Invalid choice, please type 'h' for hit or 's' for stand.")

    # Check if player busted
    if player_value > 21:
        print("You busted! Dealer wins.")
    else:
        # Dealer's turn
        print("\nDealer's turn...")
        while dealer_value < 17:
            new_card = draw_cards(deck_id, count=1)[0]
            dealer_hand.append(new_card)
            dealer_value = calculate_hand_value(dealer_hand)
            print("Dealer drew: " + new_card["value"] + " of " + new_card["suit"])

        print("\nDealer's hand:")
        for card in dealer_hand:
            print(card["value"] + " of " + card["suit"])
        print("Dealer's hand value: " + str(dealer_value))

        # Determine the winner
        if dealer_value > 21 or player_value > dealer_value:
            print("You win!")
            current_balance += bet * 2
        elif player_value < dealer_value:
            print("Dealer wins!")
        else:
            print("It's a tie! Your bet is returned.")
            current_balance += bet

    # Update the player's balance
    balances[index] = current_balance
    print("Your updated balance is: $" + str(current_balance))

    # Check if balance is zero and delete account if necessary
    if current_balance == 0:
        print("Your balance is $0. Your account will now be deleted.")
        del usernames[index]
        del passwords[index]
        del balances[index]


# Main program
def main():
    usernames = []
    passwords = []
    balances = []

    while True:
        print("Options: sign up, login, play, exit")
        option = input("What would you like to do? ").lower()

        if option == "sign up":
            sign_up(usernames, passwords, balances)
        elif option == "login":
            index, balance = login(usernames, passwords, balances)
            if index is not None:
                print("Welcome back! Your balance is $" + str(balance) + ".")
        elif option == "play":
            if len(usernames) == 0:
                print("No players are logged in. Please sign up or log in first.")
            else:
                index, _ = login(usernames, passwords, balances)
                if index is not None:
                    play_blackjack(index, usernames, passwords, balances)
        elif option == "exit":
            print("Thank you for playing. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()