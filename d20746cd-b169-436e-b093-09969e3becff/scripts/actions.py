#------------------------------------------------------------------------------
# Constant and Variables Values
#------------------------------------------------------------------------------

import re
ManaColor = "#00FF00"
PowerUpColor = "#ff0000" 
GenColor = "#27adf6"
TamperedColor="#FFFF00"
battleArray = []
manaArray = []
shieldArray = []

#------------------------------------------------------------------------------
# Table Actions
#------------------------------------------------------------------------------

def untapAll(group, x = 0, y = 0):
    mute()
    myCards = (card for card in table
                    if card.controller == me)
    for card in myCards: 
        card.orientation &= ~Rot90
    notify("{} untaps all.".format(me))

def roll6(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided dice.".format(me, n))

def diceroll20(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls {} on a 20-sided dice.".format(me, n))

def tap(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} tapped {}'.format(me, card))
    else:
        notify('{} untapped {}'.format(me, card))
def destroy(card, x = 0, y = 0):
    mute()
    Target1 = ['Aqua Commando','Aqua Knight','Aqua Infiltrator','Rapids Lurker Wwhhshrll','Cybersphere Dragon','Cyber Walker Kaylee','Queen Taniwha','Wave Lancer','Crusader Engine','Aqua Rider','Warbringer Poseidon','Aqua-Reflector Nomulos','Aqua Trooper XJ-3','Outpost Sentry']
    Target2 = ['Karate Carrot','Gasbag','Red-Eye Scorpion','Bronze-Arm Sabertooth','Manapod Beetle','Lotus Warrior','Fullmetal Lemon','Transforming Totem','Pesky Pineapple','Rapscallion','Tuber Tribe','Bloomwarden','Lore-Strider','Goop Striker','Anjak, the All-Kin','Bronze-Arm Fanatic','Bronze-Arm Renegade','Corporal Pepper','Defiant Shaman','Eternal Gaia Dragon']
    Target3 = ['Flare Inhibitor','Flamewing Pheonix','Luminous Shieldwing']

    if card.name in Target1:
       card.moveTo(me.hand)
       notify("{} moves {} back to his hand".format(me,card))
    elif card.name in Target2:
       card.highlight = ManaColor
       notify("{}'s {} becomes mana".format(me,card))
    elif card.name in Target3:
       card.isFaceUp==False
       notify("{}'s {} moves to shield zone".format(me,card))
    else:
       card.moveTo(me.Graveyard)
       notify("{} banished {}.".format(me, card))
 
def shieldblast(card, x = 0, y = 0):
    mute()
    Target1 = ['Caius of Cloud Legion','Truthseeker Forion','Justicar Arcanix','Aeronaut Glu-urrgle']
    if card.isFaceUp==False:
        card.peek()
        rnd(1,100)
        if re.search("Shield Blast", card.Rules):
            if confirm("Activate Shield Blast for {} - {} ?".format(card.Name,card.Rules)):
                card.isFaceUp=True
                rnd(1,10)
                notify("{} uses {}'s Shield Blast.".format(me, card))
                return
        card.moveTo(card.controller.hand)
        notify("{}'s shield is broken.".format(me))
    return	

def flipcard(card, x = 0, y = 0):
    mute()
    if card.isFaceUp == False: 
       card.isFaceUp = True
       notify("{} flips {} face up".format(me,card))
    else:
       card.isFaceUp = False
       notify("{} flips {} facedown".format(me,card))

def setmana(card,x=0, y=0):
    mute()
    if card.isFaceUp == True and card.owner == me and card.controller==me:
       card.highlight = ManaColor
       notify("{} puts {} into his/her Mana Zone.".format(me,card))
    else:
        notify("This card can't become mana")
        return

def genactivation(card,x=0, y=0):
    mute()
    if card.isFaceUp == True and card.controller==me:     
	  card.highlight = GenColor
	  notify("{} uses {}s effect".format(me,card))
    else:
       whisper("This isnt a valid target")		
		
def clearhighlight(card,x=0, y=0):
    mute()
    card.highlight = None
    notify("{} clears {} highlight.".format(me,card))

def givepower(card,x=0, y=0):
    mute()
    if card.isFaceUp == True and card.owner == me and card.controller==me:
       card.highlight = PowerUpColor
       notify("Your opponent uses {} for the final attack.".format(card))
    else:
        notify("This card can't be chosen")
        return

def movetograve(card, x = 0, y = 0):
    mute()
    card.moveTo(me.Graveyard)
    notify("{} moves {} to his/her Graveyard.".format(me,card))
		
def movetohand(card, x = 0, y = 0):
    mute()
    card.moveTo(me.hand)
    notify("{} moves {} to his/her hand.".format(me,card))

def movetodecktop(card, x = 0, y = 0):
    mute()
    card.moveTo(me.Library)
    notify("{} moves {} to the top of his/her deck.".format(me,card))

def movetodeckbot(card, x = 0, y = 0):
    mute()
    c= len(me.Library)
    card.moveToBottom(me.Library)
    notify("{} moves {} to the bottom of his/her deck.".format(me,card))

#------------------------------------------------------------------------------
# Functtional (Utility)
#------------------------------------------------------------------------------
def checkCardTable(card, array, x = 0, y = 0):
    ids = []
    for card in table:
        ids.append(card._id)
    for cardid in array:
        if cardid not in ids:
            array.remove(cardid)
    return array

def alignBattle(card, x = 0, y = 0, arrange = False, battleArray = []):
    if not Table.isTwoSided():  ## the case where two-sided table is disabled
        whisper("Cannot align: Two-sided table is required for card alignment.")
        return
    side = me._id
    if side == 1:
        multiplier = 1
        difference = 0
    else:
        multiplier = -1
        difference = 100
    battleArray = checkCardTable(card, battleArray)
    if not arrange:
        battleCount = 0
        for card in table:
            if card.controller == me and card._id in battleArray:
                card.moveToTable(x+70*battleCount, multiplier*y-difference, False)
                battleCount+=1

def alignMana(card, x = 0, y = 0, arrange = False, manaArray = []):
    if not Table.isTwoSided():  ## the case where two-sided table is disabled
        whisper("Cannot align: Two-sided table is required for card alignment.")
        return
    side = me._id
    if side == 1:
        multiplier = 1
        difference = 0
    else:
        multiplier = -1
        difference = 100
    manaArray = checkCardTable(card, manaArray)
    if not arrange:
        manaCount = 0
        for card in table:
            if card.controller == me and card._id in manaArray:
                card.moveToTable(x+100*manaCount, multiplier*y-difference, False)
                manaCount+=1

def alignShield(card, x = 0, y = 0, arrange = False, shieldArray = []):
    if not Table.isTwoSided():  ## the case where two-sided table is disabled
        whisper("Cannot align: Two-sided table is required for card alignment.")
        return
    side = me._id
    if side == 1:
        multiplier = 1
        difference = 0
    else:
        multiplier = -1
        difference = 100
    shieldArray = checkCardTable(card, shieldArray)
    if not arrange:
        shieldCount = 0
        for card in table:
            if card.controller == me and card._id in shieldArray:
                card.moveToTable(x+70*shieldCount, multiplier*y-difference, False)
                shieldCount+=1

#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------
def sendAllDeck(card, x = 0, y = 0):
    mute()
    for card in me.hand:
        card.moveTo(me.Library)
    notify("{} builds up his deck".format(me))
    


def play(card, x = 0, y = 0):
    mute()
    card.moveToTable(0, 0)
    notify("{} plays {} from his/her hand.".format(me, card))
    battleArray.append(card._id)
    if card._id in manaArray:
        manaArray.remove(card._id)
    if card._id in shieldArray:
        shieldArray.remove(card._id)
    alignBattle(card, -150, 5, False, battleArray)

def discard(card, x = 0, y = 0):
    mute()
    notify("{} discards {} from his/her hand.".format(me, card))
    card.moveTo(me.Graveyard)

def randomDiscard(group, x = 0, y = 0):
    mute()
    card = group.random()
    if card == None: return
    notify("{} randomly discards {}.".format(me,card))
    card.moveTo(me.Graveyard)  

def randomDiscard2(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group.random()
    toGraveyard(card, notifymute = True)
    if notifymute == False:
        rnd(1,10)
        notify("{} randomly discards {}.".format(me, card))

def randompile(group, x = 0, y = 0):
    mute()
    card = group.random()
    if card == None: return
    notify("{} randomly chooses a card from his/her Discard Pile and puts it into the Battle Zone.".format(me,card))
    card.moveToTable(0, 0, False)

def playshield(card, x = 0, y = 0):
    mute()
    card.moveToTable(0, 0, True)
    card.isFaceUp = False
    card.highlight = TamperedColor
    notify("{} sets a shield from his/her hand.".format(me))
    shieldArray.append(card._id)
    if card._id in manaArray:
        manaArray.remove(card._id)
    if card._id in battleArray:
        battleArray.remove(card._id)
    alignShield(card, -250, 100, False, shieldArray)

def discardall(group, x = 0, y = 0):
    if len(group) == 0: return
    mute()
    for card in me.hand:
        card.moveTo(me.Graveyard)
    notify("{} discards all the cards in his/her hand".format(me,card))

def playmana(card, x = 0, y = 0):
    mute()
    card.moveToTable(0,0)
    card.highlight = ManaColor
    notify("{} puts {} into his Mana Zone from his/her hand.".format(me,card))
    manaArray.append(card._id)
    if card._id in battleArray:
        battleArray.remove(card._id)
    if card._id in shieldArray:
        shieldArray.remove(card._id)
    alignMana(card, -350, 204, False, manaArray)

def showhand(group, x = 0, y = 0):
    mute()
    notify("{} shows his/her hand to the opponent.".format(me))
    notify("----------------------------------------")
    i = 0
    for card in me.hand:
        i = i+1
        notify("{}. {}".format(i,card.name))
    notify("----------------------------------------")

#------------------------------------------------------------------------------
# Deck Actions
#------------------------------------------------------------------------------

def draw(group, x = 0, y = 0):
    if len(group) == 0: return
    mute()
    group[0].moveTo(me.hand)
    notify("{} draws a card.".format(me))

def drawMany(group, count = None):
    if len(group) == 0: return
    mute()
    if count == None: count = askInteger("How many cards to draw?", 5)
    if count == None: return
    for c in group.top(count): c.moveTo(me.hand)
    notify("{} draws {} cards.".format(me, count))

def drawreveal(group,x = 0, y = 0):
    if len(group) == 0: return
    mute()
    notify("{} adds {} from his deck to his/her hand.".format(me,group[0]))
    group[0].moveTo(me.hand)

def shuffle(group):
    mute()
    if len(group) == 0: return
    group.shuffle()
    notify("{} shuffles his/her deck".format(me))

def mill(group = me.Library):
	if len(group) == 0: return
	mute()
	group[0].moveTo(me.Graveyard)
	notify("{} mills the top card from his/her Deck.".format(me))
	
def millx(group = me.Library, count = None):
    if len(group) == 0: return
    mute()
    if count == None: count = askInteger("How many cards to mill?", 2)
    if count == None: return
    else:
        for c in group.top(count): c.moveTo(me.Graveyard)
        notify("{} mills the top {} cards from his/her Deck.".format(me, count))

def setShield(group, x = 0, y = 0):
    if len(group) == 0:return
    mute()
    card = group[0]
    shieldArray.append(group[0]._id)
    if card._id in manaArray:
        manaArray.remove(card._id)
    if card._id in battleArray:
        battleArray.remove(card._id)
    card.moveToTable(0, 0, True)
    card.highlight = TamperedColor
    notify("{} sets a shield from the top of the deck.".format(me))
    alignShield(card, -250, 100, False, shieldArray)

def newcard(group, x = 0, y = 0):
    if len(group) == 0:return
    mute()
    card = group[0]
    battleArray.append(group[0]._id)
    card.moveToTable(0, 0, False)
    notify("{} puts the top card of the deck into his/her Battle Zone.".format(me))
    alignBattle(card, -150, 5, False, battleArray)

def setasMana(group, x = 0, y = 0):
    if len(group) == 0:return
    mute()
    card = group[0]
    manaArray.append(group[0]._id)
    if card._id in battleArray:
        battleArray.remove(card._id)
    if card._id in shieldArray:
        shieldArray.remove(card._id)
    card.moveToTable(0, 0, False)
    card.highlight = ManaColor
    notify("{} puts the top card of the deck into his/her Mana Zone.".format(me))
    alignMana(card, -350, 204, False, manaArray)

def resetduel(group, x = 0, y = 0):
    mute()
    for card in table:
        if card.controller == me:
           if card._id in manaArray:
               manaArray.remove(card._id)
           elif card._id in battleArray:
               battleArray.remove(card._id)
           elif card._id in shieldArray:
               shieldArray.remove(card._id)
           card.moveTo(me.Library)
    
    for card in me.graveyard:
        if card._id in manaArray:
            manaArray.remove(card._id)
        elif card._id in battleArray:
            battleArray.remove(card._id)
        elif card._id in shieldArray:
            shieldArray.remove(card._id)
        card.moveTo(me.Library)
    
    for card in me.hand:
        if card._id in manaArray:
            manaArray.remove(card._id)
        elif card._id in battleArray:
            battleArray.remove(card._id)
        elif card._id in shieldArray:
            shieldArray.remove(card._id)
        card.moveTo(me.Library)

    if len(group) == 0:return
    #group.shuffle()
    notify("{} shuffles his/her deck".format(me))
    notify("{} resets his/her side of the field".format(me))

def duelsetup2(group, x = 0, y = 0):
    mute()
    if len(group)< 10: return

    #group.shuffle()

    group[0].moveToTable(-225, 102, True)
    group[0].moveToTable(-150, 102, True)
    group[0].moveToTable(-75, 102, True)
    group[0].moveToTable(0, 102, True)
    group[0].moveToTable(75, 102, True)

    Player1 = rnd(1,6)
    notify("{} rolls a {}".format(me,Player1))
    whisper("Don't forget to setup the VEIL - top 5 cards")
	
def duelsetup(group, x = 0, y = 0):
    mute()
    if len(group)< 10: return

    side = me._id
    if side == 1:
        multiplier = 1
        difference = 0
    else:
        multiplier = -1
        difference = 100

    shieldArray.append(group[0]._id)
    group[0].moveToTable(-225, multiplier*100-difference, True)
    shieldArray.append(group[0]._id)
    group[0].moveToTable(-150, multiplier*100-difference, True)
    shieldArray.append(group[0]._id)
    group[0].moveToTable(-75, multiplier*100-difference, True)
    shieldArray.append(group[0]._id)
    group[0].moveToTable(0, multiplier*100-difference, True)
    shieldArray.append(group[0]._id)
    group[0].moveToTable(75, multiplier*100-difference, True)

    Player1 = rnd(1,6)
    notify("{} rolls a {}".format(me,Player1))
    
    group[0].moveTo(me.hand)
    group[0].moveTo(me.hand)
    group[0].moveTo(me.hand)
    group[0].moveTo(me.hand)
    group[0].moveTo(me.hand)

    notify("{} draws his/her opening hand.".format(me))
