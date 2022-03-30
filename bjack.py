import random, time, deck, beepy
 
version = '1.66'
game = True
standing, dealToPlayer, double = [False]*3
playerWins, dealerWins, playerSum, dealerSum, moves = [0]*5
cycles = 1
dealerHand, playerHand, turnCard = [], [], []
gameDeck = deck.fullDeck.copy()
money, bet = 1000, 10
 
def resetgame():
    global game, standing, moves, dealerHand, dealerSum, playerHand, playerSum, turnCard, dealToPlayer, double, cycles
    for i in range(20): print()
    game = True
    standing, dealToPlayer, double = [False]*3
    playerSum, dealerSum, moves = [0]*3
    dealerHand, playerHand, turnCard = [], [], []
    cycles += 1
 
def cardname(card): return str(card[1]) + str(card[2])
 
def printhands():
    print('dealer: {:<2s} : '.format(str(dealerSum)), end='')
    for card in dealerHand: print(cardname(card) + ' ', end='')
    if len(turnCard) > 0: print('▓▓', end='')
    print()
    print('player: {:<2s} : '.format(str(playerSum)), end='')
    for card in playerHand: print(cardname(card) + ' ', end='')
    print()
 
def sumcards():
    global dealerSum, playerSum
    thesum = 0
    for card in dealerHand:
        if card[1] == "A" and thesum + 11 > 21: cardvalue = 1
        else: cardvalue = card[0]
        thesum = thesum + cardvalue
    dealerSum = thesum
    thesum = 0
    for card in playerHand:
        if card[1] == "A" and thesum + 11 > 21: cardvalue = 1
        else: cardvalue = card[0]
        thesum = thesum + cardvalue
    playerSum = thesum
 
def dealcard(player):
    global gameDeck
    if len(gameDeck) == 0:
        gameDeck = deck.fullDeck.copy()
        print('♻ deck reshuffled')
    dealtcard = random.randrange(0, len(gameDeck))
    if player == 'dealer': dealerHand.append(gameDeck[dealtcard])
    if player == 'player': playerHand.append(gameDeck[dealtcard])
    if player == 'theTurnCard':
        turnCard.append(gameDeck[dealtcard])
        print('➥ ▓▓ to dealer')
    if player == "dealer" or player == "player": print('➥ ' + gameDeck[dealtcard][1] + gameDeck[dealtcard][2] + ' to ' + player)
    del (gameDeck[dealtcard])
 
def flipturncard():
    global turnCard
    print('➥ flipped ' + cardname(turnCard[0]))
    dealerHand.append(turnCard[0])
    turnCard = []
 
def gameovercheck():
    global game, standing, dealerSum, playerSum, playerWins, dealerWins, money
    if game is True and playerSum > 21:
        game = False
        print('\ngame over: player busts, dealer wins')
        sound('dealerwins')
        dealerWins += 1
        money -= bet
        if double: money -= bet
    if game is True and dealerSum > 21:
        game = False
        print('\ngame over: dealer busts, player wins')
        sound('playerwins')
        playerWins += 1
        money += bet
        if double: money += bet
    if game is True and standing is True and dealerSum == playerSum and dealerSum > 16:
        game = False
        print('game over: draw')
        sound('tie')
    if game is True and standing is True and playerSum > dealerSum > 16:
        game = False
        print('\ngame over: player wins')
        sound('playerwins')
        playerWins += 1
        money += bet
        if double: money += bet
    if game is True and standing is True and dealerSum > playerSum and dealerSum > 16:
        game = False
        print('\ngame over: dealer wins')
        sound('dealerwins')
        dealerWins += 1
        money -= bet
        if double: money -= bet
 
def sound(soundType):
    if soundType == 'playerwins': beepy.beep(sound='coin')
    elif soundType == 'dealerwins': beepy.beep(sound='error')
    elif soundType == 'tie': beepy.beep(sound='ping')
    elif soundType == 'blackjack': beepy.beep(sound='ready')
 
while True:
    if moves > 0: time.sleep(0.6)
    moves += 1
    if moves == 1:
        if dealerWins > 0 or playerWins > 0: winRate = round(playerWins / (dealerWins + playerWins)*100)
        else: winRate = 0
        print('--- round ' + str(cycles) + ' betting $' + str(bet) + ' of $' + str(round(money)))
        print('--- wins: ' + str(playerWins) + ' of ' + str(playerWins+dealerWins) + ' (' + str(winRate) + '%)')
        dealcard('dealer')
        dealcard('theTurnCard')
        dealcard('player')
        dealcard('player')
        sumcards()
        if((turnCard[0][0] + dealerSum) == 21) and playerSum == 21:
            game = False
            flipturncard()
            print('\ngame over: push')
            sound('tie')
        if len(turnCard) > 0 and turnCard[0][0] + dealerSum == 21:
            game = False
            flipturncard()
            print('\ngame over: dealer wins with a Blackjack')
            sound('dealerwins')
            dealerWins += 1
            money -= bet
        if playerSum == 21:
            game = False
            print('\ngame over: player wins with a Blackjack')
            sound('blackjack')
            playerWins += 1
            money += bet*1.5
    else: print('\n--- move ' + str(moves) + ' ---')
    if dealToPlayer:
        dealcard('player')
        dealToPlayer = False
    if standing is True and len(turnCard) > 0: flipturncard()
    elif game is True and standing is True and dealerSum < 17: dealcard('dealer')
    if playerSum == 21: standing = True
    sumcards()
    printhands()
    gameovercheck()
    if game is False:
        print('you have $' + str(money))
        if money < 1:
            print('\n* you are bankrupt. time to quit. *')
            sound('dealerwins')
            exit()
        choice = input('[enter] next round at $' + str(bet) + ', [c]hange bet, or [q]uit? ')
        if choice == 'q': exit()
        elif choice == 'c':
            newbet = input("how much to bet? $")
            if money >= int(newbet) > 1:
                bet = int(newbet)
                print('updated bet to ' + str(bet))
            else:
                print('\n* not enough money *')
                time.sleep(2)
            resetgame()
        else: resetgame()
    elif game is True and standing is False and moves < 2 and money >= (bet*2):
        choice = input("[s]tand, [h]it, or [d]ouble? ")
        if choice == 'h': dealToPlayer = True
        elif choice == 'd':
            dealToPlayer = True
            double = True
            standing = True
        elif choice == 's': standing = True
        else: print('what?')
    elif game is True and standing is False and moves >= 2:
        choice = input("[s]tand or [h]it? ")
        if choice == 'h': dealToPlayer = True
        elif choice == 's': standing = True
        else: print('what?')
