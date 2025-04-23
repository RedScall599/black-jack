"""
Data Structures
Student Project
Project Title:
"""
import requests
import random

url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
response = requests.get(url).json()
deck_id = response["deck_id"]
usernames = []
passwords = []
balances = []
# Draw cards
cards_url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=" + str(2)
cards_response = requests.get(cards_url).json()
hand = cards_response["cards"]

# Calculate hand value
value = 0
aces = 0
for card in hand:
    if card["value"] in ["KING", "QUEEN", "JACK"]:
        value += 10
    elif card["value"] == "ACE":
        aces += 1
        value += 11  # Assume ace is 11 initially
    else:
        value += int(card["value"])

while value > 21 and aces:
    value -= 10  # Convert one ace from 11 to 1 if value over 21
    aces -= 1

running = True

while running:
    print("Options: sign up, login, exit ")
    option = input("which would you like to do: ")
    
    ## -- Exiting -- ##
    if option == "exit":
        break
    ## -- if the user types login -- ##
    if option == "login":
        enter_username = input("enter your username")
        ## checks if the username exists ##
        if enter_username not in usernames:
 
            print("That username is incorrect or doesnt exist please try again")
            
            continue
        enter_password = input("enter your password ")
        ## checks if input for password exist ##
        if enter_password not in passwords:
 
            print("That password is incorrect or doesnt exist please try again")
            
            continue
        ## -- Balance display -- ##
        index = passwords.index(enter_password)
        
        current = balances[index] 

        print("your balance is $" + str(current))
        
        current = int(current) 
        
        spend = int(input("How much do you want to bet: "))  
        
        ##- checks if the balance is less then or equal to -##
        if spend <= current: 
 
            current -= spend 

            balances[index] = current 

            print("your new balance is $" + str(balances[index]))
            
            game_over = False
            dealer_turn = True
            while not game_over:
                
                # Start blackjack game
                print("Welcome to Blackjack!")
                
                # Draw hands for player and dealer
                player_hand = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=2").json()["cards"]
                dealer_hand = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=2").json()["cards"]
                
                # Display initial hands
                print("Player's cards:")
                for card in player_hand:
                    print(card["value"] + " of " + card["suit"])
                print()
                
                print("Dealer's cards:")
                for card in dealer_hand:
                    print(card["value"] + " of " + card["suit"])
                print()
                
                # Player's turn
                player_turn = True
                player_sum = 0
                for card in player_hand:
                    if card["value"] in ["KING", "QUEEN", "JACK"]:
                        player_sum += 10
                    elif card["value"] == "ACE":
                        player_sum += 11
                        aces += 1
                    else:
                        player_sum += int(card["value"])
                
                while player_turn:
                    print("Your current total is: " + str(player_sum))
                    choice = input("Do you want to hit or stand? (h/s): ").lower()
                    if choice == "h":
                        new_card = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=1").json()["cards"][0]
                        
                        player_hand.append(new_card)
                        print("You drew: " + new_card["value"] + " of " + new_card["suit"])
                        if new_card["value"] in ["KING", "QUEEN", "JACK"]:
                            player_sum += 10
                        elif new_card["value"] == "ACE":
                            player_sum += 11
                            aces += 1
                        else:
                            
                            player_sum += int(new_card["value"])
                
                        while player_sum > 21 and aces:
                            player_sum -= 10
                            aces -= 1
                
                        if player_sum > 21:
                            print("You busted with a total of: " + str(player_sum))
                            player_turn = False
                    elif choice == "s":
                        print("You stand with a total of: " + str(player_sum))
                        player_turn = False
                    else:
                        print("Invalid input. Please enter 'h' to hit or 's' to stand.")
                
                # Dealer's turn
                # Dealer's turn will be skipped if the player has already-
                # bust(gone over 21)
                if player_sum > 21:
                    dealer_turn = False
                dealer_sum = 0
                aces = 0
                for card in dealer_hand:
                    if card["value"] in ["KING", "QUEEN", "JACK"]:
                        dealer_sum += 10
                    elif card["value"] == "ACE":
                        dealer_sum += 11
                        aces += 1
                    else:
                        dealer_sum += int(card["value"])
                
                while dealer_sum < 17 and dealer_turn == True :
                    new_card = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=1").json()["cards"][0]
                    dealer_hand.append(new_card)
                    print("Dealer drew: " + new_card["value"] + " of " + new_card["suit"])
                    
                    if new_card["value"] in ["KING", "QUEEN", "JACK"]:
                        dealer_sum += 10
                    elif new_card["value"] == "ACE":
                        dealer_sum += 11
                        aces += 1
                    else:
                        dealer_sum += int(new_card["value"])
                
                    while dealer_sum > 21 and aces:
                        dealer_sum -= 10
                        aces -= 1
                
                print("Dealer's total is: " + str(dealer_sum))
                
                # Determine winner
                if player_sum > 21:
                    print("Dealer wins! You busted.")
                    if current == 0:
                        print("your balance is empty and your account will be deleted as a result")
                        if index < len(passwords) and index < len(balances):
                    
                            del passwords[index]
                            del usernames[index]
                            del balances[index]
                elif dealer_sum > 21:
                    print("You win! Dealer busted.")
                    current += spend
                    current += spend
                    balances[index] = current
                    print("your new balance is $" + str(balances[index]))
                elif player_sum > dealer_sum:
                    print("You win!")
                    current += spend
                    current += spend
                    balances[index] = current
                    print("your new balance is $" + str(balances[index]))
                elif player_sum < dealer_sum:
                    print("Dealer wins!")
                    print("your new balance is $" + str(balances[index]))
                    if current == 0:
                        print("your balance is empty and your account will be deleted as a result")
                        if index < len(passwords) and index < len(balances):
                    
                            del passwords[index]
                            del usernames[index]
                            del balances[index]
                else:
                    print("It's a tie!")
                    current += spend
                    balances[index] = current
                    print("your new balance is $" + str(balances[index]))
                game_over = True
    if option == "sign up":
        new_username = input("create a username : ")
        if new_username in usernames:
 
            print("That username is taken please try again")
            
            continue
        else:
            print(new_username + " is vaild")
            
            new_password = input(" create a password : ")
            if new_password in passwords:
 
                print("That password is taken please try again")
                
                continue
            else:
                ## adds the new username and password if both are not taken ##
                print(new_password + " is vaild")
                passwords.append(new_password)
                usernames.append(new_username)
                ## creates a new balance for your new account
                print("50$ is being added to your new account.")
                adding_balance = 50
                balances.append(adding_balance)