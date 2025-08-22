import random

playerHand = []
dealerHand = []
playerTotal = 0
dealerTotal = 0

def ShowHand(hand):
    print("[", end = " ")
    for x in hand:
        if x == 1:
            print("A", end = " ")
        elif x == 11:
            print("J", end = " ")
        elif x == 12:
            print("Q", end = " ")
        elif x ==13:
            print("K", end = " ")
        else:
            print (x, end = " ")
    print("]", end = " ")

def CalculateHand(hand):
    total = 0
    hasA = (1 in hand)
    for x in hand:
        if x == 11 or x == 12 or x == 13:
            total += 10
        else:
            total += x

    if total + 10 <= 21 and hasA == 1:
        total += 10
    return total

def Hit(hand):
    hand.append(random.randint(1, 13))

def DealStartingHands():
    Hit(dealerHand)
    Hit(dealerHand)

    Hit(playerHand)
    Hit(playerHand)

    global playerTotal
    global dealerTotal

    playerTotal = CalculateHand(playerHand)
    dealerTotal = CalculateHand(dealerHand)

def PlayerAction():
    global playerTotal
    playerTotal = CalculateHand(playerHand)
    print ("You have", end = " ")
    ShowHand(playerHand)
    if playerTotal > 21:
            print ("\nYou have Busted")
            exit()
    if len(playerHand) == 5:
            print ("\nYou have a Charlie's Five")
            exit()
    choice = input("[H]Hit [S]Stand ")
    if choice.lower() == "h":
        print("You Hit")
        Hit(playerHand)
        PlayerAction()
    elif choice.lower() != "s":
        PlayerAction()

def DealerAction():
    global dealerTotal
    dealerTotal = CalculateHand(dealerHand)
    print("Dealer has ", end = "")
    ShowHand(dealerHand)
    if dealerTotal > 21:
        print ("\nDealer has Busted")
        exit()
    if dealerTotal < 17:
        print("\nDealer Hit")
        Hit(dealerHand)
        DealerAction()
    else:
        print("\nDealer Stands")


#main
DealStartingHands()

print("Dealer has ", end = "")
ShowHand(dealerHand)
print("")

PlayerAction()
DealerAction()

if playerTotal > dealerTotal:
    print("You Won")
elif playerTotal < dealerTotal:
    print("You lost")
else:
    print("Tie")


#coded by Bingo