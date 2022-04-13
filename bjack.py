import random, time, deck

# customizable settings
defaultbet = 10         # how much bet to start with
defaultmoney = 1000     # how much money to start with
delaytime = 0.5         # seconds to pause between card deals
scrollamount = 20       # how many lines to 'clear' the screen

version = '1.76'
game = True
standing, dealToPlayer, double = [False] * 3
playerwins, dealerwins, playersum, dealersum, moves, money, bet = [0] * 7
cycles = 1
dealerhand, playerhand, turncard = [], [], []
gameDeck = deck.fullDeck.copy()
savegamefile = 'savegame.txt'

def savegame():
    global bet, money
    f = open(savegamefile, "w+")
    f.writelines(str(round(bet))+'\n')
    f.writelines(str(round(money)))
    f.close()

def loadgame():
    global bet, money
    f = open(savegamefile, "r")
    lines = f.readlines()
    f.close()
    bet = int(lines[0])
    money = int(lines[1])

def resetgame(howdeep=''):
    global bet, money, gameDeck, game, standing, moves, dealerhand, dealersum, playerhand, playersum, turncard, dealToPlayer, double, cycles
    for i in range(scrollamount): print()
    game = True
    standing, dealToPlayer, double = [False]*3
    playersum, dealersum, moves = [0] * 3
    dealerhand, playerhand, turncard = [], [], []
    cycles += 1
    if howdeep == 'deeply':
        bet = defaultbet
        money = defaultmoney
        gameDeck = deck.fullDeck.copy()
    savegame()

def cardname(card): return str(card[1]) + str(card[2])

def printhands():
    print('dealer: {:<2s} : '.format(str(dealersum)), end='')
    for card in dealerhand: print(cardname(card) + ' ', end='')
    if len(turncard) > 0: print('▓▓', end='')
    print()
    print('player: {:<2s} : '.format(str(playersum)), end='')
    for card in playerhand: print(cardname(card) + ' ', end='')
    print()

def sumcards():
    global dealersum, playersum
    thesum = 0
    for card in dealerhand:
        if card[1] == "A" and thesum + 11 > 21: cardvalue = 1
        else: cardvalue = card[0]
        thesum = thesum + cardvalue
    dealersum = thesum
    thesum = 0
    for card in playerhand:
        if card[1] == "A" and thesum + 11 > 21: cardvalue = 1
        else: cardvalue = card[0]
        thesum = thesum + cardvalue
    playersum = thesum

def dealcard(player):
    global gameDeck
    if len(gameDeck) == 0:
        gameDeck = deck.fullDeck.copy()
        print('♻ deck reshuffled')
    dealtcard = random.randrange(0, len(gameDeck))
    if player == 'dealer': dealerhand.append(gameDeck[dealtcard])
    if player == 'player': playerhand.append(gameDeck[dealtcard])
    if player == 'theTurnCard':
        turncard.append(gameDeck[dealtcard])
        print('➥ ▓▓ to dealer')
    if player == "dealer" or player == "player": print('➥ ' + gameDeck[dealtcard][1] + gameDeck[dealtcard][2] + ' to ' + player)
    del (gameDeck[dealtcard])

def flipturncard():
    global turncard
    print('➥ flipped ' + cardname(turncard[0]))
    dealerhand.append(turncard[0])
    turncard = []

def gameovercheck():
    global game, standing, dealersum, playersum, playerwins, dealerwins, money
    if game is True and playersum > 21:
        game = False
        print('\ngame over: player busts, dealer wins\n')
        dealerwins += 1
        money -= bet
        if double: money -= bet
    if game is True and dealersum > 21:
        game = False
        print('\ngame over: dealer busts, player wins\n')
        playerwins += 1
        money += bet
        if double: money += bet
    if game is True and standing is True and dealersum == playersum and dealersum > 16:
        game = False
        print('\ngame over: draw\n')
    if game is True and standing is True and playersum > dealersum > 16:
        game = False
        print('\ngame over: player wins\n')
        playerwins += 1
        money += bet
        if double: money += bet
    if game is True and standing is True and dealersum > playersum and dealersum > 16:
        game = False
        print('\ngame over: dealer wins\n')
        dealerwins += 1
        money -= bet
        if double: money -= bet

loadgame()

while True:
    if moves > 0: time.sleep(delaytime)
    moves += 1
    if moves == 1:
        if dealerwins > 0 or playerwins > 0: winRate = round(playerwins / (dealerwins + playerwins) * 100)
        else: winRate = 0
        print('--- round ' + str(cycles) + ' betting $' + str(bet) + ' of $' + str(round(int(money))))
        print('--- wins: ' + str(playerwins) + ' of ' + str(playerwins + dealerwins) + ' (' + str(winRate) + '%)')
        dealcard('dealer')
        dealcard('theTurnCard')
        dealcard('player')
        dealcard('player')
        sumcards()
        if((turncard[0][0] + dealersum) == 21) and playersum == 21:
            game = False
            flipturncard()
            print('\ngame over: push\n')
        if len(turncard) > 0 and turncard[0][0] + dealersum == 21:
            game = False
            flipturncard()
            print('\ngame over: dealer wins with a Blackjack\n')
            dealerwins += 1
            money -= bet
        if playersum == 21:
            game = False
            print('\ngame over: player wins with a Blackjack\n')
            playerwins += 1
            money += bet*1.5
    else: print('\n--- move ' + str(moves) + ' ---')
    if dealToPlayer:
        dealcard('player')
        dealToPlayer = False
    if standing is True and len(turncard) > 0: flipturncard()
    elif game is True and standing is True and dealersum < 17: dealcard('dealer')
    sumcards()
    printhands()
    if playersum == 21: standing = True
    gameovercheck()
    if game is False:
        print('you have $' + str(round(money)))
        if money < 1:
            print('\n* you are bankrupt. time to quit! *\n')
            resetgame('deeply')
            exit()
        choice = input('[enter] next round at $' + str(bet) + ', [c]hange bet, [r]eset, or [q]uit? ')
        if choice == 'q':
            savegame()
            exit()
        elif choice == 'c':
            newbet = input("how much to bet? $")
            if money >= int(newbet) > 1:
                bet = int(newbet)
                print('updated bet to ' + str(bet))
            else:
                print('\n* not enough money *\n')
                time.sleep(2)
            resetgame()
        elif choice == 'r':
            resetconfirm = input('are you sure you want to start over with $' + str(defaultmoney) + '? [y/n]')
            if resetconfirm == 'y' or resetconfirm == 'Y':
                resetgame('deeply')
            else:
                resetgame()
        elif choice =='' : resetgame()
        else: print('what?')
    elif game is True and standing is False and moves == 1 and money >= (bet*2):
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
